from run_cycle import main as previous_cycle
from task_evaluator import evaluate_tasks
from replanner import replan_if_needed
from executor import execute_one_task


def main():
    print("Running base autonomous cycle...")
    previous_cycle()

    print("Evaluating tasks...")
    useful, doubtful = evaluate_tasks()

    print("Replanning if needed...")
    changed, actions = replan_if_needed(useful, doubtful)
    if changed:
        print("Replanning applied:")
        for a in actions:
            print(f"- {a}")

    if not useful:
        print("No useful tasks detected after evaluation. Skipping execution.")
        return

    print("Executing one useful task...")
    task = execute_one_task()
    if task:
        print(f"Executed: {task['id']}")
    else:
        print("No task executed")


if __name__ == "__main__":
    main()
