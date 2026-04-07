import json
import hashlib
from pathlib import Path

TASK_QUEUE = Path("state/task_queue.json")
INTERPRETATION = Path("state/goal_interpretation.json")
REPORT = Path("reports/planning_report.md")
PLAN_META = Path("state/plan_meta.json")


def _load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def _signature_from_interpretation(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def build_initial_tasks(goal_text: str):
    interpretation = _load_json(INTERPRETATION, {
        "primary_goal": "Objetivo no definido",
        "deliverables": [],
        "constraints": [],
        "behavior_requirements": [],
        "test_data": [],
        "success_expectations": [],
        "operational_instruction": "",
        "subgoals": []
    })

    primary_goal = interpretation.get("primary_goal") or "Objetivo no definido"
    deliverables = interpretation.get("deliverables", [])
    constraints = interpretation.get("constraints", [])
    behavior_requirements = interpretation.get("behavior_requirements", [])
    success_expectations = interpretation.get("success_expectations", [])
    test_data = interpretation.get("test_data", [])

    tasks = [
        {
            "id": "task-interpret-goal",
            "title": "Interpretar objetivo actual",
            "status": "pending",
            "reason": "Necesario para convertir la instrucción del usuario en plan operativo",
            "derived_from": primary_goal,
            "priority": "high",
            "category": "core"
        },
        {
            "id": "task-build-plan",
            "title": "Construir plan inicial",
            "status": "pending",
            "reason": "Necesario para organizar la ejecución autónoma",
            "derived_from": primary_goal,
            "priority": "high",
            "category": "core"
        },
        {
            "id": "task-define-checks",
            "title": "Definir comprobaciones de consecución",
            "status": "pending",
            "reason": "Necesario para justificar cumplimiento futuro del objetivo",
            "derived_from": primary_goal,
            "priority": "high",
            "category": "verification"
        }
    ]

    for index, item in enumerate(deliverables, start=1):
        tasks.append({
            "id": f"task-deliverable-{index}",
            "title": f"Implementar entregable {index}",
            "status": "pending",
            "reason": "Entregable detectado en la interpretación estructurada del objetivo",
            "derived_from": item,
            "priority": "high" if index <= 3 else "medium",
            "category": "deliverable"
        })

    if constraints:
        tasks.append({
            "id": "task-check-constraints",
            "title": "Verificar restricciones activas",
            "status": "pending",
            "reason": "Hay restricciones detectadas que deben respetarse durante la ejecución",
            "derived_from": "; ".join(constraints),
            "priority": "high",
            "category": "constraints"
        })

    if behavior_requirements:
        tasks.append({
            "id": "task-check-behavior",
            "title": "Verificar requisitos de comportamiento",
            "status": "pending",
            "reason": "El sistema debe respetar los requisitos de comportamiento definidos por el usuario",
            "derived_from": "; ".join(behavior_requirements),
            "priority": "medium",
            "category": "behavior"
        })

    if success_expectations:
        tasks.append({
            "id": "task-map-success-criteria",
            "title": "Mapear criterio de éxito a comprobaciones",
            "status": "pending",
            "reason": "Necesario para alinear el cierre con el criterio de éxito esperado",
            "derived_from": "; ".join(success_expectations),
            "priority": "medium",
            "category": "verification"
        })

    if test_data:
        tasks.append({
            "id": "task-materialize-test-data",
            "title": "Materializar datos de prueba",
            "status": "pending",
            "reason": "Hay datos de prueba sugeridos que pueden convertirse en artefactos ejecutables",
            "derived_from": "; ".join(test_data),
            "priority": "medium",
            "category": "test_data"
        })

    signature = _signature_from_interpretation(interpretation)
    meta = {
        "interpretation_signature": signature,
        "primary_goal": primary_goal,
        "task_count": len(tasks)
    }
    PLAN_META.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")

    lines = ["# Planning Report", "", f"Primary goal: {primary_goal}", "", f"Interpretation signature: {signature}", ""]
    if deliverables:
        lines.append("## Deliverables")
        lines.extend([f"- {d}" for d in deliverables])
        lines.append("")
    if constraints:
        lines.append("## Constraints")
        lines.extend([f"- {c}" for c in constraints])
        lines.append("")
    if behavior_requirements:
        lines.append("## Behavior requirements")
        lines.extend([f"- {b}" for b in behavior_requirements])
        lines.append("")
    if success_expectations:
        lines.append("## Success expectations")
        lines.extend([f"- {s}" for s in success_expectations])
        lines.append("")
    if test_data:
        lines.append("## Test data")
        lines.extend([f"- {t}" for t in test_data])
        lines.append("")
    lines.append("## Planned tasks")
    lines.extend([f"- {t['id']}: {t['title']} [{t['priority']}] ({t['category']})" for t in tasks])
    REPORT.write_text("\n".join(lines) + "\n")

    return {"tasks": tasks}


def write_task_queue(task_data):
    TASK_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    TASK_QUEUE.write_text(json.dumps(task_data, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    raise SystemExit("planner_V3.py is a library module")
