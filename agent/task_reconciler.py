import json
from pathlib import Path

TASK_QUEUE = Path("state/task_queue.json")
REPORT = Path("reports/task_reconciliation_report.md")

ARTIFACT_EXPECTATIONS = {
    "task-deliverable-1": ["artifacts/travel_ideas/travel_ideas_input.md"],
    "task-deliverable-2": [
        "artifacts/travel_ideas/travel_ideas_input.md",
        "artifacts/travel_ideas/parse_travel_ideas.py",
        "artifacts/travel_ideas/travel_ideas.json",
    ],
    "task-deliverable-3": [
        "artifacts/travel_ideas/travel_ideas_input.md",
        "artifacts/travel_ideas/parse_travel_ideas.py",
        "artifacts/travel_ideas/travel_ideas.json",
        "artifacts/travel_ideas/validate_travel_ideas.py",
        "artifacts/travel_ideas/validation_report.json",
    ],
    "task-deliverable-4": ["artifacts/travel_ideas/prioritize_travel_ideas.py"],
    "task-deliverable-5": ["artifacts/travel_ideas/final_report.md"],
    "task-deliverable-6": ["artifacts/travel_ideas/checks.md"],
}


def _load_queue():
    if not TASK_QUEUE.exists():
        return {"tasks": []}
    return json.loads(TASK_QUEUE.read_text())


def _save_queue(data):
    TASK_QUEUE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def reconcile_tasks():
    data = _load_queue()
    reopened = []

    for task in data.get("tasks", []):
        if task.get("status") != "done":
            continue

        task_id = task.get("id", "")
        note = (task.get("execution_note") or "").lower()

        if "without artifact" in note:
            task["status"] = "pending"
            task["execution_note"] = "Reopened by reconciler: previous completion lacked real artifact"
            reopened.append((task_id, "explicit_without_artifact_note"))
            continue

        expected_files = ARTIFACT_EXPECTATIONS.get(task_id, [])
        if expected_files and not all(Path(p).exists() for p in expected_files):
            task["status"] = "pending"
            task["execution_note"] = "Reopened by reconciler: expected artifact set is incomplete"
            reopened.append((task_id, "missing_expected_artifacts"))

    _save_queue(data)

    lines = ["# Task Reconciliation Report", ""]
    if reopened:
        lines.append("## Reopened tasks")
        for task_id, reason in reopened:
            lines.append(f"- {task_id}: {reason}")
    else:
        lines.append("- No task reconciliation changes were needed")
    lines.append("")
    REPORT.write_text("\n".join(lines))

    return reopened


if __name__ == "__main__":
    print(reconcile_tasks())
