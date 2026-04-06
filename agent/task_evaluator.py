import json
from pathlib import Path

TASK_QUEUE = Path("state/task_queue.json")
REPORT = Path("reports/task_evaluation.md")


def load_tasks():
    if not TASK_QUEUE.exists():
        return {"tasks": []}
    return json.loads(TASK_QUEUE.read_text())


def evaluate_tasks():
    data = load_tasks()
    useful = []
    doubtful = []

    for task in data.get("tasks", []):
        title = task.get("title", "").lower()
        reason = task.get("reason", "").lower()

        if any(keyword in title or keyword in reason for keyword in ["objetivo", "plan", "comprob", "valid", "usuario"]):
            useful.append(task)
        else:
            doubtful.append(task)

    lines = ["# Task Evaluation", "", f"Useful tasks: {len(useful)}", f"Doubtful tasks: {len(doubtful)}", ""]
    if useful:
        lines.append("## Useful")
        lines.extend([f"- {t['id']}: {t['title']}" for t in useful])
        lines.append("")
    if doubtful:
        lines.append("## Doubtful")
        lines.extend([f"- {t['id']}: {t['title']}" for t in doubtful])
        lines.append("")

    REPORT.write_text("\n".join(lines))
    return useful, doubtful


if __name__ == "__main__":
    evaluate_tasks()
