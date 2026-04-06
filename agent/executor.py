import json
from pathlib import Path

TASK_QUEUE = Path("state/task_queue.json")
LOG_FILE = Path("logs/audit.log")
REPORT = Path("reports/execution_report.md")

PRIORITY_ORDER = {
    "high": 0,
    "medium": 1,
    "low": 2
}


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


def _task_sort_key(task):
    status_rank = 0 if task.get("status") == "pending" else 1
    priority_rank = PRIORITY_ORDER.get(task.get("priority", "medium"), 1)
    return (status_rank, priority_rank, task.get("id", ""))


def choose_next_task(data):
    pending = [t for t in data.get("tasks", []) if t.get("status") == "pending"]
    if not pending:
        return None
    pending.sort(key=_task_sort_key)
    return pending[0]


def execute_one_task():
    data = load_tasks()
    task = choose_next_task(data)

    if not task:
        log("No pending tasks.")
        REPORT.write_text("# Execution Report\n\n- No pending tasks were available for execution.\n")
        return None

    for item in data.get("tasks", []):
        if item.get("id") == task.get("id"):
            item["status"] = "done"
            item["execution_note"] = "Executed by priority-aware executor"
            break

    log(f"Executed task: {task['id']} - {task['title']} [priority={task.get('priority', 'medium')}]")
    save_tasks(data)
    REPORT.write_text(
        "# Execution Report\n\n"
        f"- Executed task: {task['id']}\n"
        f"- Title: {task['title']}\n"
        f"- Priority: {task.get('priority', 'medium')}\n"
    )
    return task


if __name__ == "__main__":
    execute_one_task()
