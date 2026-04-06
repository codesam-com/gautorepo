from run_cycle import main as previous_cycle
from success_criteria_builder import build_success_criteria
from goal_evidence_collector import collect_evidence
from goal_verifier_V2 import verify_goal
from stop_manager import enter_stop_mode


def main():
    print("Running base autonomous cycle...")
    previous_cycle()

    print("Rebuilding success criteria...")
    build_success_criteria()

    print("Collecting updated evidence...")
    collect_evidence()

    print("Running improved goal verification...")
    achieved = verify_goal()

    if achieved:
        print("Goal VERIFIED with stricter logic")
        enter_stop_mode("Goal achieved with verified criteria and no pending tasks")
    else:
        print("Goal still not achieved under stricter verification")


if __name__ == "__main__":
    main()
