from pathlib import Path
import json

GOAL_FILE = Path("user/goal.md")
CRITERIA_FILE = Path("state/success_criteria.json")
REPORT = Path("reports/success_criteria.md")


def read_goal():
    if not GOAL_FILE.exists():
        return ""
    return GOAL_FILE.read_text()


def build_success_criteria():
    goal = read_goal().strip()
    criteria = {
        "goal_detected": bool(goal),
        "criteria": [
            {
                "id": "criterion-goal-present",
                "description": "Existe un objetivo explícito del usuario",
                "status": "pass" if bool(goal) else "fail"
            },
            {
                "id": "criterion-plan-exists",
                "description": "Existe un plan operativo derivado del objetivo",
                "status": "unknown"
            },
            {
                "id": "criterion-checks-defined",
                "description": "Existen comprobaciones de consecución del objetivo",
                "status": "unknown"
            }
        ]
    }

    CRITERIA_FILE.parent.mkdir(parents=True, exist_ok=True)
    CRITERIA_FILE.write_text(json.dumps(criteria, indent=2, ensure_ascii=False) + "\n")

    lines = ["# Success Criteria", ""]
    for item in criteria["criteria"]:
        lines.append(f"- {item['id']}: {item['description']} [{item['status']}]")
    REPORT.write_text("\n".join(lines) + "\n")
    return criteria


if __name__ == "__main__":
    build_success_criteria()
