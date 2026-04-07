import json
from pathlib import Path

TASK_QUEUE = Path("state/task_queue.json")
LOG_FILE = Path("logs/audit.log")
REPORT = Path("reports/execution_report.md")

PRIORITY_ORDER = {
    "high": 0,
    "medium": 1,
    "low": 2,
}

CATEGORY_ORDER = {
    "deliverable": 0,
    "verification": 1,
    "constraints": 2,
    "test_data": 3,
    "behavior": 4,
    "core": 5,
}

CORE_BOOTSTRAP_TASKS = {
    "task-interpret-goal",
    "task-build-plan",
    "task-define-checks",
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


def _bootstrap_complete(tasks):
    completed = {t.get("id") for t in tasks if t.get("status") == "done"}
    return "task-build-plan" in completed


def _task_sort_key(task, bootstrap_complete: bool):
    priority_rank = PRIORITY_ORDER.get(task.get("priority", "medium"), 1)
    category = task.get("category", "deliverable")
    category_rank = CATEGORY_ORDER.get(category, 9)

    if not bootstrap_complete:
        if task.get("id") == "task-build-plan":
            return (-1, 0, 0, task.get("id", ""))
        if task.get("id") in CORE_BOOTSTRAP_TASKS:
            return (0, category_rank, priority_rank, task.get("id", ""))

    if bootstrap_complete:
        if category == "deliverable":
            return (0, priority_rank, category_rank, task.get("id", ""))
        if category in {"verification", "constraints", "test_data"}:
            return (1, priority_rank, category_rank, task.get("id", ""))
        if category in {"behavior", "core"}:
            return (2, priority_rank, category_rank, task.get("id", ""))

    return (3, priority_rank, category_rank, task.get("id", ""))


def choose_next_task(data):
    pending = [t for t in data.get("tasks", []) if t.get("status") == "pending"]
    if not pending:
        return None

    bootstrap_complete = _bootstrap_complete(data.get("tasks", []))
    pending.sort(key=lambda task: _task_sort_key(task, bootstrap_complete))
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
            item["execution_note"] = "Executed by product-oriented executor"
            break

    log(
        f"Executed task: {task['id']} - {task['title']} "
        f"[priority={task.get('priority', 'medium')}, category={task.get('category', 'unknown')}]"
    )
    save_tasks(data)
    REPORT.write_text(
        "# Execution Report\n\n"
        f"- Executed task: {task['id']}\n"
        f"- Title: {task['title']}\n"
        f"- Priority: {task.get('priority', 'medium')}\n"
        f"- Category: {task.get('category', 'unknown')}\n"
    )
    return task


if __name__ == "__main__":
    execute_one_task()
