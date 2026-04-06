import json
from pathlib import Path

TASK_QUEUE = Path("state/task_queue.json")
INTERPRETATION = Path("state/goal_interpretation.json")
REPORT = Path("reports/planning_report.md")


def _load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def build_initial_tasks(goal_text: str):
    interpretation = _load_json(INTERPRETATION, {
        "primary_goal": "Objetivo no definido",
        "constraints": [],
        "subgoals": []
    })

    primary_goal = interpretation.get("primary_goal") or "Objetivo no definido"
    subgoals = interpretation.get("subgoals", [])
    constraints = interpretation.get("constraints", [])

    tasks = [
        {
            "id": "task-interpret-goal",
            "title": "Interpretar objetivo actual",
            "status": "pending",
            "reason": "Necesario para convertir la instrucción del usuario en plan operativo",
            "derived_from": primary_goal,
            "priority": "high"
        },
        {
            "id": "task-build-plan",
            "title": "Construir plan inicial",
            "status": "pending",
            "reason": "Necesario para organizar la ejecución autónoma",
            "derived_from": primary_goal,
            "priority": "high"
        },
        {
            "id": "task-define-checks",
            "title": "Definir comprobaciones de consecución",
            "status": "pending",
            "reason": "Necesario para justificar cumplimiento futuro del objetivo",
            "derived_from": primary_goal,
            "priority": "high"
        }
    ]

    for index, subgoal in enumerate(subgoals, start=1):
        tasks.append({
            "id": f"task-subgoal-{index}",
            "title": f"Trabajar subobjetivo {index}",
            "status": "pending",
            "reason": "Subobjetivo detectado en la interpretación semántica",
            "derived_from": subgoal,
            "priority": "medium"
        })

    if constraints:
        tasks.append({
            "id": "task-check-constraints",
            "title": "Verificar restricciones activas",
            "status": "pending",
            "reason": "Hay restricciones detectadas que deben respetarse durante la ejecución",
            "derived_from": "; ".join(constraints),
            "priority": "high"
        })

    lines = ["# Planning Report", "", f"Primary goal: {primary_goal}", ""]
    if constraints:
        lines.append("## Constraints")
        lines.extend([f"- {c}" for c in constraints])
        lines.append("")
    if subgoals:
        lines.append("## Subgoals")
        lines.extend([f"- {s}" for s in subgoals])
        lines.append("")
    lines.append("## Planned tasks")
    lines.extend([f"- {t['id']}: {t['title']} [{t['priority']}]" for t in tasks])
    REPORT.write_text("\n".join(lines) + "\n")

    return {"tasks": tasks}


def write_task_queue(task_data):
    TASK_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    TASK_QUEUE.write_text(json.dumps(task_data, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    raise SystemExit("planner_V2.py is a library module")
