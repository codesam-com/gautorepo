import json
from pathlib import Path

TASK_QUEUE = Path("state/task_queue.json")


def build_initial_tasks(goal_text: str):
    summary = goal_text.strip().splitlines()
    first_meaningful = next((line.strip() for line in summary if line.strip() and not line.startswith("#")), "Objetivo no definido")

    return {
        "tasks": [
            {
                "id": "task-interpret-goal",
                "title": "Interpretar objetivo actual",
                "status": "pending",
                "reason": "Necesario para convertir la instrucción del usuario en plan operativo",
                "derived_from": first_meaningful
            },
            {
                "id": "task-build-plan",
                "title": "Construir plan inicial",
                "status": "pending",
                "reason": "Necesario para organizar la ejecución autónoma",
                "derived_from": first_meaningful
            },
            {
                "id": "task-define-checks",
                "title": "Definir comprobaciones de consecución",
                "status": "pending",
                "reason": "Necesario para justificar cumplimiento futuro del objetivo",
                "derived_from": first_meaningful
            }
        ]
    }


def write_task_queue(task_data):
    TASK_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    TASK_QUEUE.write_text(json.dumps(task_data, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    raise SystemExit("planner.py is a library module")
