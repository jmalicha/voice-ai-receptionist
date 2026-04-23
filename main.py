import logging
import re
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from services.claude_service import get_lily_response
from services.email_service import send_call_summary_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Rose and Bloom Voice AI Receptionist")


@app.get("/")
async def health_check():
    return {"status": "ok", "receptionist": "Lily is online"}


@app.post("/webhook")
async def vapi_webhook(request: Request):
    """
    Receives conversation turns from Vapi.
    Vapi sends a JSON payload containing the message history.
    We return Lily's next response in the format Vapi expects.
    """
    try:
        body = await request.json()
        logger.info(f"Webhook received: {body}")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    # Vapi sends the conversation under body["message"]["artifact"]["messagesOpenAIFormatted"]
    # or body["message"]["messages"] depending on assistant config.
    # We support both structures.
    message_payload = body.get("message", {})
    message_type = message_payload.get("type", "")

    # Only respond to conversation turns
    if message_type not in ("assistant-request", "function-call", ""):
        return JSONResponse(content={"result": ""})

    # Extract conversation history in OpenAI format (role/content pairs)
    conversation = (
        message_payload.get("artifact", {}).get("messagesOpenAIFormatted")
        or message_payload.get("messages")
        or []
    )

    # Filter to only user and assistant roles (Claude API requirement)
    filtered = [
        {"role": m["role"], "content": m["content"]}
        for m in conversation
        if m.get("role") in ("user", "assistant") and m.get("content")
    ]

    # First turn: no messages yet, return greeting directly without calling Claude
    if not filtered:
        lily_response = "Thank you for calling Rose and Bloom Flowers. This is Lily, how can I help you today?"
        logger.info(f"Lily greets: {lily_response}")
        return JSONResponse(content={"result": lily_response})

    lily_response = get_lily_response(filtered)
    logger.info(f"Lily responds: {lily_response}")

    # Vapi expects the response in this format
    return JSONResponse(content={"result": lily_response})


@app.post("/call-ended")
async def call_ended(request: Request):
    """
    Receives all Vapi server events. Only processes end-of-call-report type.
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    message_payload = body.get("message", {})
    message_type = message_payload.get("type", "")

    # Ignore all events except the end-of-call report
    if message_type != "end-of-call-report":
        logger.info(f"Ignoring event type: {message_type}")
        return JSONResponse(content={"status": "ignored"})

    logger.info(f"End-of-call report received: {body}")

    call_data = message_payload.get("call", {})

    # Extract caller phone number
    caller_number = (
        call_data.get("customer", {}).get("number")
        or call_data.get("phoneNumber", {}).get("number")
        or "Unknown number"
    )

    analysis = message_payload.get("analysis", {}) or {}
    artifact = message_payload.get("artifact", {}) or {}
    messages = artifact.get("messages", []) or []

    # Build readable transcript from conversation messages
    user_messages = [
        m.get("message", "") for m in messages if m.get("role") == "user" and m.get("message")
    ]
    bot_messages = [
        m.get("message", "") for m in messages if m.get("role") == "bot" and m.get("message")
    ]
    full_transcript = "\n".join([
        f"{'Caller' if m.get('role') == 'user' else 'Lily'}: {m.get('message','')}"
        for m in messages
        if m.get("role") in ("user", "bot") and m.get("message")
    ])

    # Use Vapi's AI summary if available, otherwise fall back to transcript
    summary = analysis.get("summary") or full_transcript or "No summary available."

    # Extract caller name from structuredData first, then scan transcript
    structured = analysis.get("structuredData") or {}
    caller_name = structured.get("callerName") or structured.get("name") or None
    action_needed = structured.get("actionNeeded") or "None"

    # If no structured name, scan user messages for "my name is X" patterns
    if not caller_name:
        for msg in user_messages:
            match = re.search(
                r"(?:my name is|this is|it'?s|i'?m)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
                msg, re.IGNORECASE
            )
            if match:
                caller_name = match.group(1).strip()
                break

    # Extract callback number from transcript (number caller gave verbally, not their caller ID)
    callback_number = None
    for msg in user_messages:
        match = re.search(r"\b(\d{3}[\s\-.]?\d{3}[\s\-.]?\d{4})\b", msg)
        if match:
            callback_number = match.group(1)
            break

    # Use the callback number they gave verbally if different from caller ID
    contact_number = callback_number if callback_number else caller_number

    send_call_summary_email(
        caller_number=contact_number,
        caller_name=caller_name,
        summary=summary[:600],
        action_needed=action_needed,
    )
    logger.info("Email summary sent to owner")

    return JSONResponse(content={"status": "received"})
