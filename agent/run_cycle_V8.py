from run_cycle import main as previous_cycle
from success_criteria_builder import build_success_criteria
from goal_evidence_collector import collect_evidence
from goal_verifier import verify_goal
from stop_manager import enter_stop_mode


def main():
    print("Running base autonomous cycle...")
    previous_cycle()

    print("Building success criteria...")
    criteria = build_success_criteria()

    print("Collecting evidence...")
    collect_evidence()

    print("Verifying goal against criteria...")
    achieved = verify_goal()

    if achieved:
        enter_stop_mode("Goal achieved with evidence")
        print("System entering STOP mode")
    else:
        print("Goal not yet achieved")


if __name__ == "__main__":
    main()
