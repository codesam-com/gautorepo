from pathlib import Path
import json

OUTPUT = Path("state/self_patch_plan.json")
REPORT = Path("reports/self_patch_plan.md")


def build_self_patch_plan():
    plan = {
        "proposals": [
            {
                "id": "improve_goal_verification",
                "target": "agent/goal_verifier.py",
                "kind": "upgrade_candidate",
                "reason": "A stricter verifier exists and should become canonical later"
            },
            {
                "id": "review_cycle_cohesion",
                "target": "agent/run_cycle.py",
                "kind": "review_candidate",
                "reason": "The canonical cycle should stay aligned with the latest capabilities"
            }
        ]
    }

    OUTPUT.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")

    lines = ["# Self Patch Plan", ""]
    for item in plan["proposals"]:
        lines.append(f"- {item['id']} -> {item['target']} ({item['kind']})")
        lines.append(f"  - Reason: {item['reason']}")
    lines.append("")
    REPORT.write_text("\n".join(lines))
    return plan


if __name__ == "__main__":
    build_self_patch_plan()
