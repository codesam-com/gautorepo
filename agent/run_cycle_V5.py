from run_cycle import main as previous_cycle
from task_evaluator import evaluate_tasks
from executor import execute_one_task


def main():
    print("Running base autonomous cycle...")
    previous_cycle()

    print("Evaluating tasks before execution...")
    useful, doubtful = evaluate_tasks()

    if not useful:
        print("No useful tasks detected. Skipping execution.")
        return

    print("Executing one useful task...")
    task = execute_one_task()
    if task:
        print(f"Executed: {task['id']}")
    else:
        print("No task executed")


if __name__ == "__main__":
    main()
