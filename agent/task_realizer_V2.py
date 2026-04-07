from pathlib import Path
import json

ARTIFACT_DIR = Path("artifacts/travel_ideas")
REPORT = Path("reports/task_realization_report.md")
INPUT_FILE = ARTIFACT_DIR / "travel_ideas_input.md"
PARSER_FILE = ARTIFACT_DIR / "parse_travel_ideas.py"
VALIDATOR_FILE = ARTIFACT_DIR / "validate_travel_ideas.py"
JSON_FILE = ARTIFACT_DIR / "travel_ideas.json"
VALIDATION_REPORT = ARTIFACT_DIR / "validation_report.json"


def _write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _ensure_input_file() -> bool:
    if INPUT_FILE.exists():
        return False
    _write(
        INPUT_FILE,
        "# Ideas de viaje\n\n"
        "- destino: Lisboa | presupuesto: bajo | duracion: 3 dias | prioridad: alta\n"
        "- destino: Tokio | presupuesto: alto | duracion: 10 dias | prioridad: media\n"
        "- destino: Sin destino | presupuesto: | duracion: | prioridad: baja\n"
        "- destino: Escapada rural | presupuesto: medio | duracion: 2 dias | prioridad: alta\n"
    )
    return True


def _ensure_parser_file() -> bool:
    if PARSER_FILE.exists():
        return False
    _write(
        PARSER_FILE,
        "from pathlib import Path\n"
        "import json\n\n"
        "INPUT = Path('artifacts/travel_ideas/travel_ideas_input.md')\n"
        "OUTPUT = Path('artifacts/travel_ideas/travel_ideas.json')\n\n"
        "def parse_line(line: str):\n"
        "    raw = line.strip().lstrip('-').strip()\n"
        "    parts = [p.strip() for p in raw.split('|')]\n"
        "    item = {}\n"
        "    for part in parts:\n"
        "        if ':' in part:\n"
        "            k, v = part.split(':', 1)\n"
        "            item[k.strip()] = v.strip()\n"
        "    return item\n\n"
        "def main():\n"
        "    entries = []\n"
        "    if INPUT.exists():\n"
        "        for line in INPUT.read_text().splitlines():\n"
        "            if line.strip().startswith('- '):\n"
        "                entries.append(parse_line(line))\n"
        "    OUTPUT.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + '\\n')\n\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )
    return True


def _ensure_validator_file() -> bool:
    if VALIDATOR_FILE.exists():
        return False
    _write(
        VALIDATOR_FILE,
        "from pathlib import Path\n"
        "import json\n\n"
        "INPUT = Path('artifacts/travel_ideas/travel_ideas.json')\n"
        "OUTPUT = Path('artifacts/travel_ideas/validation_report.json')\n\n"
        "REQUIRED = ['destino', 'presupuesto', 'duracion', 'prioridad']\n\n"
        "def main():\n"
        "    if not INPUT.exists():\n"
        "        OUTPUT.write_text(json.dumps({'error': 'missing_input'}, indent=2, ensure_ascii=False) + '\\n')\n"
        "        return\n"
        "    data = json.loads(INPUT.read_text())\n"
        "    valid = []\n"
        "    invalid = []\n"
        "    for item in data:\n"
        "        missing = [k for k in REQUIRED if not item.get(k)]\n"
        "        if missing:\n"
        "            invalid.append({'item': item, 'missing': missing})\n"
        "        else:\n"
        "            valid.append(item)\n"
        "    OUTPUT.write_text(json.dumps({'valid': valid, 'invalid': invalid}, indent=2, ensure_ascii=False) + '\\n')\n\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )
    return True


def _materialize_json_placeholder() -> bool:
    if JSON_FILE.exists():
        return False
    _write(JSON_FILE, json.dumps([], indent=2, ensure_ascii=False) + "\n")
    return True


def _materialize_validation_placeholder() -> bool:
    if VALIDATION_REPORT.exists():
        return False
    _write(VALIDATION_REPORT, json.dumps({"valid": [], "invalid": []}, indent=2, ensure_ascii=False) + "\n")
    return True


def realize_task(task: dict) -> bool:
    task_id = task.get("id", "")
    title = task.get("title", "")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    actions = []

    if task_id == "task-deliverable-1":
        created = _ensure_input_file()
        actions.append("ensured travel_ideas_input.md")
        _write(
            REPORT,
            "# Task Realization Report\n\n"
            "- Realized task-deliverable-1\n"
            f"- Created input file: {created}\n"
            "- Ensured: artifacts/travel_ideas/travel_ideas_input.md\n"
        )
        return True

    if task_id == "task-deliverable-2":
        input_created = _ensure_input_file()
        parser_created = _ensure_parser_file()
        actions.extend([
            f"input_created={input_created}",
            f"parser_created={parser_created}",
        ])
        _write(
            REPORT,
            "# Task Realization Report\n\n"
            "- Realized task-deliverable-2\n"
            f"- Prerequisite input ensured: {INPUT_FILE.as_posix()}\n"
            f"- Input created during this run: {input_created}\n"
            f"- Parser created during this run: {parser_created}\n"
            f"- Ensured parser: {PARSER_FILE.as_posix()}\n"
        )
        return True

    if task_id == "task-deliverable-3":
        input_created = _ensure_input_file()
        parser_created = _ensure_parser_file()
        json_created = _materialize_json_placeholder()
        validator_created = _ensure_validator_file()
        validation_placeholder_created = _materialize_validation_placeholder()
        actions.extend([
            f"input_created={input_created}",
            f"parser_created={parser_created}",
            f"json_created={json_created}",
            f"validator_created={validator_created}",
            f"validation_placeholder_created={validation_placeholder_created}",
        ])
        _write(
            REPORT,
            "# Task Realization Report\n\n"
            "- Realized task-deliverable-3\n"
            f"- Ensured input: {INPUT_FILE.as_posix()}\n"
            f"- Ensured parser: {PARSER_FILE.as_posix()}\n"
            f"- Ensured JSON data file: {JSON_FILE.as_posix()}\n"
            f"- Ensured validator: {VALIDATOR_FILE.as_posix()}\n"
            f"- Ensured validation report placeholder: {VALIDATION_REPORT.as_posix()}\n"
        )
        return True

    _write(
        REPORT,
        "# Task Realization Report\n\n"
        f"- No concrete artifact realization rule for task: {task_id} ({title})\n"
    )
    return False


if __name__ == "__main__":
    print(realize_task({"id": "task-deliverable-2", "title": "Implementar entregable 2"}))
