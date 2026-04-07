from pathlib import Path
import json

GOAL_FILE = Path("user/goal.md")
OUTPUT = Path("state/goal_interpretation.json")
REPORT = Path("reports/goal_interpretation.md")

SECTION_NAMES = {
    "objetivo principal": "primary_goal_section",
    "entregables esperados": "deliverables",
    "restricciones obligatorias": "constraints",
    "requisitos de comportamiento del repo": "behavior_requirements",
    "datos de prueba sugeridos": "test_data",
    "criterio de éxito esperado": "success_expectations",
    "instrucción operativa": "operational_instruction",
}


def read_goal():
    if not GOAL_FILE.exists():
        return ""
    return GOAL_FILE.read_text().strip()


def _normalize_heading(line: str) -> str:
    return line.strip().lstrip("#").strip().lower()


def _clean_item(line: str) -> str:
    return line.strip().lstrip("- ").strip()


def interpret_goal():
    goal_text = read_goal()
    lines = goal_text.splitlines()

    sections = {value: [] for value in SECTION_NAMES.values()}
    current_section = None

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue

        normalized = _normalize_heading(line)
        if normalized in SECTION_NAMES:
            current_section = SECTION_NAMES[normalized]
            continue

        if line.strip().startswith("#"):
            continue

        if current_section is None:
            continue

        sections[current_section].append(_clean_item(line))

    primary_goal_candidates = sections["primary_goal_section"]
    primary_goal = primary_goal_candidates[0] if primary_goal_candidates else "No explicit goal detected"

    deliverables = [item for item in sections["deliverables"] if item]
    constraints = [item for item in sections["constraints"] if item]
    behavior_requirements = [item for item in sections["behavior_requirements"] if item]
    test_data = [item for item in sections["test_data"] if item]
    success_expectations = [item for item in sections["success_expectations"] if item]
    operational_instruction = " ".join(sections["operational_instruction"]).strip()

    subgoals = []
    if primary_goal != "No explicit goal detected":
        subgoals.append(primary_goal)
    subgoals.extend(deliverables)

    data = {
        "primary_goal": primary_goal,
        "deliverables": deliverables,
        "constraints": constraints,
        "behavior_requirements": behavior_requirements,
        "test_data": test_data,
        "success_expectations": success_expectations,
        "operational_instruction": operational_instruction,
        "subgoals": subgoals,
        "has_goal": primary_goal != "No explicit goal detected"
    }

    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    report_lines = [
        "# Goal Interpretation",
        "",
        "## Primary goal",
        primary_goal,
        "",
        "## Deliverables",
    ]
    report_lines.extend([f"- {item}" for item in deliverables] or ["- None detected"])
    report_lines.extend([
        "",
        "## Constraints",
    ])
    report_lines.extend([f"- {item}" for item in constraints] or ["- None detected"])
    report_lines.extend([
        "",
        "## Behavior requirements",
    ])
    report_lines.extend([f"- {item}" for item in behavior_requirements] or ["- None detected"])
    report_lines.extend([
        "",
        "## Test data",
    ])
    report_lines.extend([f"- {item}" for item in test_data] or ["- None detected"])
    report_lines.extend([
        "",
        "## Success expectations",
    ])
    report_lines.extend([f"- {item}" for item in success_expectations] or ["- None detected"])
    report_lines.extend([
        "",
        "## Operational instruction",
        operational_instruction or "None detected",
        "",
    ])

    REPORT.write_text("\n".join(report_lines))
    return data


if __name__ == "__main__":
    interpret_goal()
