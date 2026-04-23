import requests
from config import RESEND_API_KEY, OWNER_EMAIL

def send_call_summary_email(
    caller_number: str,
    caller_name: str | None,
    summary: str,
    action_needed: str,
) -> None:
    name_line = caller_name if caller_name else "Unknown"
    action_line = action_needed if action_needed else "None"

    subject = f"New Call from {name_line} ({caller_number}) - Rose and Bloom Flowers"
    body = (
        f"Hi,\n\n"
        f"Lily just handled a call at Rose and Bloom Flowers. Here are the details:\n\n"
        f"-------------------------------------------\n"
        f"CALLER INFORMATION\n"
        f"-------------------------------------------\n"
        f"Name:         {name_line}\n"
        f"Phone Number: {caller_number}\n\n"
        f"-------------------------------------------\n"
        f"CALL SUMMARY\n"
        f"-------------------------------------------\n"
        f"{summary}\n\n"
        f"-------------------------------------------\n"
        f"ACTION NEEDED\n"
        f"-------------------------------------------\n"
        f"{action_line}\n\n"
        f"-------------------------------------------\n"
        f"Please follow up with the caller as soon as possible if action is required.\n\n"
        f"- Lily, Rose and Bloom Flowers Virtual Receptionist"
    )

    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": "Lily - Rose and Bloom <onboarding@resend.dev>",
            "to": [OWNER_EMAIL],
            "subject": subject,
            "text": body,
        },
    )

    if response.status_code not in (200, 201):
        raise RuntimeError(f"Resend API error {response.status_code}: {response.text}")
