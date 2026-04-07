import json
import hashlib
from pathlib import Path

PLAN_META = Path("state/plan_meta.json")
INTERPRETATION = Path("state/goal_interpretation.json")
TASK_QUEUE = Path("state/task_queue.json")


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


def should_rebuild_plan() -> tuple[bool, str]:
    interpretation = _load_json(INTERPRETATION, {})
    plan_meta = _load_json(PLAN_META, {})
    task_queue = _load_json(TASK_QUEUE, {"tasks": []})

    if not interpretation:
        return True, "missing_interpretation"

    current_signature = _signature_from_interpretation(interpretation)
    saved_signature = plan_meta.get("interpretation_signature")

    if not task_queue.get("tasks"):
        return True, "empty_task_queue"

    if not saved_signature:
        return True, "missing_plan_meta"

    if saved_signature != current_signature:
        return True, "interpretation_signature_changed"

    return False, "plan_up_to_date"


if __name__ == "__main__":
    rebuild, reason = should_rebuild_plan()
    print({"rebuild": rebuild, "reason": reason})
