from engine import detect_change
from planner import build_initial_tasks, write_task_queue
from executor import execute_one_task
from evaluator import evaluate
from blocker_detector import detect_blockers
from goal_verifier import verify_goal
from self_cleaner import inspect_repo_hygiene
from user_request_manager import set_ready, request_user_action
from stop_manager import enter_stop_mode


def main():
    changed, goal = detect_change()

    if changed:
        print("Goal changed. Rebuilding plan...")
        tasks = build_initial_tasks(goal)
        write_task_queue(tasks)

    print("Running repository hygiene inspection...")
    hygiene_findings = inspect_repo_hygiene()
    legacy_present = [f for f in hygiene_findings if f.startswith("LEGACY_WORKFLOW_PRESENT")]

    print("Running blocker detection...")
    blockers = detect_blockers()

    print("Running self evaluation...")
    evaluate()

    print("Checking goal completion...")
    achieved = verify_goal()
    if achieved:
        enter_stop_mode("Goal verification succeeded")
        print("Entered stop mode")
        return

    if blockers:
        request_user_action(
            request_id="REQ-BLOCKED-001",
            title="Resolve blocked external task",
            why_needed="The system detected one or more blocked tasks that appear to depend on an external action or permission.",
            steps=[
                "Review status/user_instructions.md in future improved cycles",
                "Provide the required free permission or resource if requested",
                "Wait for the next cycle so the system can verify the change"
            ],
            verification="The system will re-check blocked tasks and confirm whether execution can continue"
        )
        print("User action requested due to blockers")
        return

    if legacy_present:
        print("Legacy workflow files detected. Manual cleanup should be requested through audit output.")

    set_ready()

    print("Executing one task if justified...")
    task = execute_one_task()
    if task:
        print(f"Executed: {task['id']}")
    else:
        print("Nothing to execute")


if __name__ == "__main__":
    main()
