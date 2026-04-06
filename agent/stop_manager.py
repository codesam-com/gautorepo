import json
from pathlib import Path

STATE = Path("status/state.json")
GOAL_REPORT = Path("status/goal_achieved.json")


def enter_stop_mode(reason: str):
    state = {
        "mode": "GOAL_ACHIEVED_STOPPED",
        "objective_status": "achieved",
        "autonomous_changes_enabled": False,
        "reason": reason
    }
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")

    GOAL_REPORT.write_text(json.dumps({
        "status": "achieved",
        "reason": reason
    }, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    enter_stop_mode("manual test")
