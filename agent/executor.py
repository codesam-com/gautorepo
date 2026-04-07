import json
from pathlib import Path
from task_realizer import realize_task

TASK_QUEUE = Path("state/task_queue.json")
LOG_FILE = Path("logs/audit.log")
REPORT = Path("reports/execution_report.md")


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


def choose_next_task(data):
    pending = [t for t in data.get("tasks", []) if t.get("status") == "pending"]
    if not pending:
        return None

    # simple priority: deliverables first
    pending.sort(key=lambda t: (t.get("category") != "deliverable", t.get("priority") != "high"))
    return pending[0]


def execute_one_task():
    data = load_tasks()
    task = choose_next_task(data)

    if not task:
        REPORT.write_text("# Execution Report\n\n- No pending tasks\n")
        return None

    realized = realize_task(task)

    for item in data.get("tasks", []):
        if item.get("id") == task.get("id"):
            item["status"] = "done"
            item["execution_note"] = "Executed with artifact realization" if realized else "Executed without artifact"
            break

    save_tasks(data)

    REPORT.write_text(
        "# Execution Report\n\n"
        f"- Executed task: {task['id']}\n"
        f"- Title: {task['title']}\n"
        f"- Category: {task.get('category')}\n"
        f"- Realized artifact: {realized}\n"
    )

    log(f"Executed {task['id']} | realized={realized}")

    return task


if __name__ == "__main__":
    execute_one_task()
