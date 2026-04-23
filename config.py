import os
from dotenv import load_dotenv

load_dotenv()

REQUIRED_VARS = [
    "ANTHROPIC_API_KEY",
    "VAPI_API_KEY",
    "TWILIO_ACCOUNT_SID",
    "TWILIO_AUTH_TOKEN",
    "TWILIO_PHONE_NUMBER",
    "OWNER_PHONE_NUMBER",
    "RESEND_API_KEY",
    "OWNER_EMAIL",
]

for var in REQUIRED_VARS:
    if not os.getenv(var):
        raise EnvironmentError(f"Missing required environment variable: {var}")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
OWNER_PHONE_NUMBER = os.getenv("OWNER_PHONE_NUMBER")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
OWNER_EMAIL = os.getenv("OWNER_EMAIL")
