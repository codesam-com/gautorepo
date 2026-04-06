from pathlib import Path
import json

GOAL_FILE = Path("user/goal.md")
OUTPUT = Path("state/goal_interpretation.json")
REPORT = Path("reports/goal_interpretation.md")


def read_goal():
    if not GOAL_FILE.exists():
        return ""
    return GOAL_FILE.read_text().strip()


def interpret_goal():
    goal_text = read_goal()
    lines = [line.strip() for line in goal_text.splitlines() if line.strip() and not line.strip().startswith("#")]

    primary_goal = lines[0] if lines else "No explicit goal detected"
    constraints = [line for line in lines[1:] if any(word in line.lower() for word in ["no ", "sin ", "gratis", "billing", "prioridad", "restric", "prohib"])]
    subgoals = [line for line in lines[1:] if line not in constraints]

    data = {
        "primary_goal": primary_goal,
        "constraints": constraints,
        "subgoals": subgoals,
        "has_goal": primary_goal != "No explicit goal detected"
    }

    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    report_lines = [
        "# Goal Interpretation",
        "",
        f"## Primary goal\n{primary_goal}",
        "",
        "## Constraints",
    ]
    report_lines.extend([f"- {c}" for c in constraints] or ["- None detected"])
    report_lines.append("")
    report_lines.append("## Subgoals")
    report_lines.extend([f"- {s}" for s in subgoals] or ["- None detected"])
    report_lines.append("")

    REPORT.write_text("\n".join(report_lines))
    return data


if __name__ == "__main__":
    interpret_goal()
