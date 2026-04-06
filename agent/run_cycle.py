from run_cycle import main as previous_cycle
from self_patch_planner import build_self_patch_plan


def main():
    print("Running base autonomous cycle...")
    previous_cycle()

    print("Planning self modifications...")
    plan = build_self_patch_plan()

    for item in plan.get("proposals", []):
        print(f"Self-improvement candidate: {item['id']} -> {item['target']}")


if __name__ == "__main__":
    main()
