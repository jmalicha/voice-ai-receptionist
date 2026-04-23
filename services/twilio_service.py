from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, OWNER_PHONE_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_call_summary_sms(
    caller_number: str,
    caller_name: str | None,
    summary: str,
    action_needed: str,
) -> None:
    name_line = caller_name if caller_name else "Unknown"
    action_line = action_needed if action_needed else "None"

    message_body = (
        f"New call from {caller_number}.\n"
        f"Caller: {name_line}.\n"
        f"Summary: {summary}\n"
        f"Action needed: {action_line}"
    )

    client.messages.create(
        body=message_body,
        from_=TWILIO_PHONE_NUMBER,
        to=OWNER_PHONE_NUMBER,
    )
