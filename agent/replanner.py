import json
from pathlib import Path

TASK_QUEUE = Path("state/task_queue.json")
REPORT = Path("reports/replanning_report.md")


def load_tasks():
    if not TASK_QUEUE.exists():
        return {"tasks": []}
    return json.loads(TASK_QUEUE.read_text())


def save_tasks(data):
    TASK_QUEUE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def replan_if_needed(useful, doubtful):
    data = load_tasks()
    changed = False
    actions = []

    if useful:
        for task in data.get("tasks", []):
            if task.get("status") == "pending" and task.get("id") == useful[0].get("id"):
                task["priority"] = "high"
                changed = True
                actions.append(f"Prioritized useful task: {task['id']}")
                break

    if doubtful and len(doubtful) >= len(useful):
        new_task = {
            "id": "task-review-strategy",
            "title": "Revisar estrategia actual",
            "status": "pending",
            "reason": "Hay demasiadas tareas dudosas respecto a las útiles"
        }
        existing_ids = {t.get("id") for t in data.get("tasks", [])}
        if new_task["id"] not in existing_ids:
            data.setdefault("tasks", []).insert(0, new_task)
            changed = True
            actions.append("Inserted strategic review task")

    if changed:
        save_tasks(data)

    lines = ["# Replanning Report", ""]
    if actions:
        lines.extend([f"- {a}" for a in actions])
    else:
        lines.append("- No replanning changes were needed")
    lines.append("")
    REPORT.write_text("\n".join(lines))
    return changed, actions


if __name__ == "__main__":
    replan_if_needed([], [])
