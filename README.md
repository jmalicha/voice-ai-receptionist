# Voice AI Receptionist - Rose and Bloom Flowers

I built a fully functional AI voice receptionist named **Lily** for a fictitious flower shop called Rose and Bloom Flowers in Grand Rapids, Michigan.

Lily answers incoming calls, handles common customer questions, collects caller information, and sends the business owner a detailed email summary after every call - all without any human involvement.

This is one of my portfolio projects. I built it to demonstrate how small businesses can use AI and voice technology to automate their front desk operations.

---

## What It Does

1. A customer calls the business phone number
2. Lily answers and handles the entire conversation using natural speech
3. She answers questions about hours, services, and pricing
4. If she does not know something, she takes down the caller's name and number for a follow-up
5. When the call ends, the business owner receives a detailed email with the caller's info, a summary of the conversation, and any action needed

---

## Tech Stack

| Layer | Technology |
|---|---|
| Voice and call handling | Vapi.ai |
| AI brain | Anthropic Claude (claude-haiku-4-5) |
| SMS infrastructure | Twilio |
| Email notifications | Resend |
| Backend server | Python / FastAPI |
| Local tunnel (development) | ngrok |

---

## Project Structure

```
voice-ai-receptionist/
├── .env.example            # Template for required environment variables
├── .gitignore
├── README.md
├── requirements.txt
├── main.py                 # FastAPI app - webhook and call-ended endpoints
├── config.py               # Loads and validates all environment variables
├── prompts/
│   └── system_prompt.txt   # Lily's personality, knowledge, and conversation rules
└── services/
    ├── __init__.py
    ├── claude_service.py   # Calls Anthropic API for AI responses
    ├── twilio_service.py   # Twilio SMS integration
    └── email_service.py    # Resend email notification after each call
```

---

## How I Built It

Vapi handles the voice layer - speech to text and text to speech. When a call comes in, Vapi sends the conversation to my FastAPI server. I use Claude as the AI brain, with a custom system prompt that gives Lily her personality and knowledge about the business. When the call ends, Vapi sends an end-of-call report to my server, which parses the transcript for the caller's name and contact number and sends the owner a formatted email via Resend.

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/jmalicha/voice-ai-receptionist.git
cd voice-ai-receptionist
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up your environment variables

```bash
cp .env.example .env
```

Fill in your credentials in `.env`:

```
ANTHROPIC_API_KEY=your_anthropic_api_key
VAPI_API_KEY=your_vapi_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
OWNER_PHONE_NUMBER=owner_phone_number
RESEND_API_KEY=your_resend_api_key
OWNER_EMAIL=owner_email_address
```

### 4. Run the server

```bash
uvicorn main:app --reload --port 8000
```

### 5. Expose your local server with ngrok

```bash
ngrok http 8000
```

Copy the HTTPS URL ngrok gives you - you will need it for the Vapi configuration below.

---

## Connecting to Vapi

1. Log in to [vapi.ai](https://vapi.ai)
2. Create an assistant using the Anthropic provider and paste in the system prompt from `prompts/system_prompt.txt`
3. Set the server URL to: `https://your-ngrok-url/call-ended`
4. Add end call phrases: `bye bye`, `goodbye`, `have a wonderful day`
5. Connect your Twilio phone number to the assistant
6. Call the number and Lily will answer

---

## Environment Variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude |
| `VAPI_API_KEY` | Vapi.ai API key |
| `TWILIO_ACCOUNT_SID` | Twilio account SID |
| `TWILIO_AUTH_TOKEN` | Twilio auth token |
| `TWILIO_PHONE_NUMBER` | Twilio phone number (E.164 format) |
| `OWNER_PHONE_NUMBER` | Business owner's phone number |
| `RESEND_API_KEY` | Resend API key for email notifications |
| `OWNER_EMAIL` | Email address to receive call summaries |

---

## About Me

I'm Joyce Malicha, a developer focused on building practical AI solutions. This project is part of my portfolio.

- GitHub: [github.com/jmalicha](https://github.com/jmalicha)
- LinkedIn: [linkedin.com/in/jmalicha](https://linkedin.com/in/jmalicha)
