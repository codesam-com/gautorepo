import json
from pathlib import Path

NEEDS_USER_ACTION = Path("status/needs_user_action.json")
READY = Path("status/ready.json")
USER_INSTRUCTIONS = Path("status/user_instructions.md")


def set_ready(message: str = "System does not require user input at this time"):
    READY.write_text(json.dumps({
        "needs_user_action": False,
        "message": message
    }, indent=2, ensure_ascii=False) + "\n")

    NEEDS_USER_ACTION.write_text(json.dumps({
        "needs_user_action": False,
        "requests": []
    }, indent=2, ensure_ascii=False) + "\n")

    USER_INSTRUCTIONS.write_text("# No action needed from the user\n\nThe system can continue autonomously at this time.\n")


def request_user_action(request_id: str, title: str, why_needed: str, steps: list[str], verification: str):
    payload = {
        "needs_user_action": True,
        "requests": [
            {
                "id": request_id,
                "title": title,
                "why_needed": why_needed,
                "verification": verification
            }
        ]
    }
    NEEDS_USER_ACTION.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")

    rendered_steps = "\n".join(f"{i+1}. {step}" for i, step in enumerate(steps))
    USER_INSTRUCTIONS.write_text(
        "# Action needed from the user\n\n"
        f"## What is needed\n{title}\n\n"
        f"## Why it is needed\n{why_needed}\n\n"
        f"## Steps\n{rendered_steps}\n\n"
        f"## How the system will verify it\n{verification}\n"
    )

    READY.write_text(json.dumps({
        "needs_user_action": True,
        "message": "System is waiting for a user action or permission"
    }, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    set_ready()
