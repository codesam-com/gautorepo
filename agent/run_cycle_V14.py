from engine import detect_change
from goal_interpreter import interpret_goal
from planner import build_initial_tasks, write_task_queue
from plan_sync import should_rebuild_plan
from task_reconciler import reconcile_tasks

from self_cleaner import inspect_repo_hygiene
from manual_cleanup_advisor import generate_cleanup_requests
from blocker_detector import detect_blockers
from evaluator import evaluate
from task_evaluator import evaluate_tasks
from replanner import replan_if_needed
from success_criteria_builder import build_success_criteria
from goal_evidence_collector import collect_evidence
from goal_verifier import verify_goal
from user_request_manager import set_ready, request_user_action
from stop_manager import enter_stop_mode
from executor import execute_one_task
from toolmaker import create_tool_if_needed
from self_improver import analyze_self
from self_patch_planner import build_self_patch_plan


def main():
    print("Starting autonomous cycle V14...")

    changed, goal = detect_change()

    print("Interpreting goal...")
    interpretation = interpret_goal()
    print(f"Primary goal: {interpretation.get('primary_goal')}")

    rebuild, reason = should_rebuild_plan()

    if changed or rebuild:
        print(f"Rebuilding task plan (reason: {reason})...")
        tasks = build_initial_tasks(goal)
        write_task_queue(tasks)

    print("Reconciling task queue...")
    reopened = reconcile_tasks()
    for item in reopened:
        print(f"Reopened task: {item}")

    print("Inspecting repository hygiene...")
    hygiene_findings = inspect_repo_hygiene()
    for finding in hygiene_findings:
        print(finding)

    print("Generating manual cleanup requests...")
    cleanup_requests = generate_cleanup_requests()
    for request in cleanup_requests:
        print(request)

    print("Detecting blockers...")
    blockers = detect_blockers()
    if blockers:
        request_user_action(
            request_id="REQ-BLOCKED-001",
            title="Resolve blocked external task",
            why_needed="The system detected blocked tasks that appear to require an external action or permission.",
            steps=[
                "Review the task queue and blocker report",
                "Provide the free permission or resource requested by the system if applicable",
                "Let the next cycle verify whether the blocker is resolved"
            ],
            verification="The system will re-check blocked tasks and confirm whether execution can continue"
        )
        print(f"Blocked tasks detected: {len(blockers)}")
        return

    print("Running self evaluation...")
    evaluate()

    print("Evaluating tasks...")
    useful, doubtful = evaluate_tasks()

    print("Replanning if needed...")
    changed_plan, replan_actions = replan_if_needed(useful, doubtful)
    if changed_plan:
        for action in replan_actions:
            print(action)

    print("Ensuring helper tool availability...")
    created, tool_path = create_tool_if_needed(
        tool_name="basic_analysis_tool",
        purpose="Provide basic structured analysis capability"
    )
    print(f"Tool status: {'created' if created else 'already_exists'} -> {tool_path}")

    set_ready()

    if useful:
        print("Executing one useful task...")
        task = execute_one_task()
        if task:
            print(f"Executed: {task['id']}")
    else:
        print("No useful tasks detected. Skipping execution.")

    print("Building success criteria...")
    build_success_criteria()

    print("Collecting evidence...")
    collect_evidence()

    print("Running self improvement analysis...")
    improvements = analyze_self()
    for item in improvements:
        print(f"Improvement insight: {item}")

    print("Planning self modifications...")
    patch_plan = build_self_patch_plan()
    for item in patch_plan.get("proposals", []):
        print(f"Self-improvement candidate: {item['id']} -> {item['target']}")

    print("Verifying goal...")
    achieved = verify_goal()
    if achieved:
        enter_stop_mode("Goal achieved with verified criteria and no pending tasks")
        print("Entered stop mode")
    else:
        print("Goal not yet achieved")


if __name__ == "__main__":
    main()
