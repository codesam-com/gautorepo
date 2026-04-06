from engine import detect_change
from planner import build_initial_tasks, write_task_queue
from executor import execute_one_task


def main():
    changed, goal = detect_change()

    if changed:
        print("Rebuilding plan...")
        tasks = build_initial_tasks(goal)
        write_task_queue(tasks)

    task = execute_one_task()

    if task:
        print(f"Executed: {task['id']}")
    else:
        print("Nothing to execute")


if __name__ == "__main__":
    main()
