import os
import anthropic
from config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "system_prompt.txt")

def load_system_prompt() -> str:
    with open(SYSTEM_PROMPT_PATH, "r") as f:
        return f.read().strip()

def get_lily_response(conversation_history: list[dict]) -> str:
    system_prompt = load_system_prompt()

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            system=system_prompt,
            messages=conversation_history,
        )
        return response.content[0].text.strip()
    except anthropic.BadRequestError as e:
        raise RuntimeError(f"Anthropic API bad request: {e}") from e
    except anthropic.AuthenticationError as e:
        raise RuntimeError(f"Anthropic API authentication failed: {e}") from e
    except anthropic.APIStatusError as e:
        raise RuntimeError(f"Anthropic API error {e.status_code}: {e.message}") from e
