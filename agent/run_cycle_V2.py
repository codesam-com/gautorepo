from engine import detect_change
from planner import build_initial_tasks, write_task_queue
from executor import execute_one_task
from evaluator import evaluate
from blocker_detector import detect_blockers
from goal_verifier import verify_goal
from self_cleaner import inspect_repo_hygiene


def main():
    changed, goal = detect_change()

    if changed:
        print("Goal changed. Rebuilding plan...")
        tasks = build_initial_tasks(goal)
        write_task_queue(tasks)

    print("Running self-clean inspection...")
    hygiene_findings = inspect_repo_hygiene()
    for finding in hygiene_findings:
        print(finding)

    print("Running blocker detection...")
    blockers = detect_blockers()
    if blockers:
        print(f"Blocked tasks detected: {len(blockers)}")
    else:
        print("No blockers detected")

    print("Running self-evaluation...")
    evaluate()

    print("Checking goal completion...")
    achieved = verify_goal()
    if achieved:
        print("Goal verified as achieved. Stop mode should be entered.")
        return

    print("Executing one task if justified...")
    task = execute_one_task()
    if task:
        print(f"Executed: {task['id']}")
    else:
        print("Nothing to execute")


if __name__ == "__main__":
    main()
