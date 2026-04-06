from pathlib import Path
import json

CRITERIA_FILE = Path("state/success_criteria.json")
EVIDENCE_REPORT = Path("reports/goal_evidence.md")
TASK_QUEUE = Path("state/task_queue.json")
INTERPRETATION_FILE = Path("state/goal_interpretation.json")
REPORT = Path("reports/goal_completion_report.md")
STATUS = Path("status/goal_achieved.json")


def _load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def verify_goal():
    criteria = _load_json(CRITERIA_FILE, {"criteria": []})
    task_data = _load_json(TASK_QUEUE, {"tasks": []})
    interpretation = _load_json(INTERPRETATION_FILE, {"has_goal": False, "primary_goal": "unknown"})
    evidence_text = EVIDENCE_REPORT.read_text() if EVIDENCE_REPORT.exists() else ""

    criteria_items = criteria.get("criteria", [])
    goal_present = bool(interpretation.get("has_goal")) and any(
        item.get("id") == "criterion-goal-present" and item.get("status") == "pass"
        for item in criteria_items
    )
    evidence_present = bool(evidence_text.strip())
    pending_tasks = [t for t in task_data.get("tasks", []) if t.get("status") == "pending"]
    completed_tasks = [t for t in task_data.get("tasks", []) if t.get("status") == "done"]

    achieved = bool(goal_present and evidence_present and not pending_tasks and completed_tasks)

    lines = [
        "# Goal Completion Report",
        "",
        f"Primary goal interpreted: {interpretation.get('primary_goal', 'unknown')}",
        "",
        f"Status: {'VERIFIED' if achieved else 'NOT VERIFIED'}",
        "",
        "## Verification summary",
        f"- Goal interpretation present: {interpretation.get('has_goal', False)}",
        f"- Goal present criterion passed: {goal_present}",
        f"- Evidence present: {evidence_present}",
        f"- Pending tasks remaining: {len(pending_tasks)}",
        f"- Completed tasks recorded: {len(completed_tasks)}",
        "",
    ]

    if pending_tasks:
        lines.append("## Pending tasks blocking completion")
        for task in pending_tasks:
            lines.append(f"- {task.get('id')}: {task.get('title')}")
        lines.append("")

    REPORT.write_text("\n".join(lines))
    STATUS.write_text(json.dumps({
        "status": "achieved" if achieved else "not_achieved",
        "primary_goal": interpretation.get("primary_goal", "unknown"),
        "goal_present": goal_present,
        "evidence_present": evidence_present,
        "pending_tasks": len(pending_tasks),
        "completed_tasks": len(completed_tasks)
    }, indent=2, ensure_ascii=False) + "\n")
    return achieved


if __name__ == "__main__":
    verify_goal()
