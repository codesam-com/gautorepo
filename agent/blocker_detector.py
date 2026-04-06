from pathlib import Path
import json

TASK_QUEUE = Path("state/task_queue.json")
BLOCKED = Path("state/blocked_tasks.json")


def detect_blockers():
    if not TASK_QUEUE.exists():
        return []

    data = json.loads(TASK_QUEUE.read_text())
    blocked = []

    for task in data.get("tasks", []):
        if task.get("status") == "pending" and "external" in task.get("title", "").lower():
            blocked.append(task)

    BLOCKED.write_text(json.dumps({"blocked": blocked}, indent=2, ensure_ascii=False))
    return blocked


if __name__ == "__main__":
    detect_blockers()
