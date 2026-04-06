import json
from pathlib import Path

TASK_QUEUE = Path("state/task_queue.json")
LOG_FILE = Path("logs/audit.log")


def load_tasks():
    if not TASK_QUEUE.exists():
        return {"tasks": []}
    return json.loads(TASK_QUEUE.read_text())


def save_tasks(data):
    TASK_QUEUE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def log(message):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")


def execute_one_task():
    data = load_tasks()

    for task in data.get("tasks", []):
        if task["status"] == "pending":
            task["status"] = "done"
            log(f"Executed task: {task['id']} - {task['title']}")
            save_tasks(data)
            return task

    log("No pending tasks.")
    return None


if __name__ == "__main__":
    execute_one_task()
