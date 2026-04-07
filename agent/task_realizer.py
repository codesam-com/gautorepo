from pathlib import Path
import json
import subprocess
import sys

ARTIFACT_DIR = Path("artifacts/travel_ideas")
REPORT = Path("reports/task_realization_report.md")
INPUT_FILE = ARTIFACT_DIR / "travel_ideas_input.md"
PARSER_FILE = ARTIFACT_DIR / "parse_travel_ideas.py"
VALIDATOR_FILE = ARTIFACT_DIR / "validate_travel_ideas.py"
PRIORITIZER_FILE = ARTIFACT_DIR / "prioritize_travel_ideas.py"
JSON_FILE = ARTIFACT_DIR / "travel_ideas.json"
VALIDATION_REPORT = ARTIFACT_DIR / "validation_report.json"
RANKING_FILE = ARTIFACT_DIR / "prioritized_travel_ideas.json"


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


def _ensure_prioritizer_file() -> bool:
    if PRIORITIZER_FILE.exists():
        return False
    _write(
        PRIORITIZER_FILE,
        "from pathlib import Path\n"
        "import json\n\n"
        "INPUT = Path('artifacts/travel_ideas/validation_report.json')\n"
        "OUTPUT = Path('artifacts/travel_ideas/prioritized_travel_ideas.json')\n\n"
        "PRIORITY_SCORE = {'alta': 3, 'media': 2, 'baja': 1}\n"
        "BUDGET_SCORE = {'bajo': 3, 'medio': 2, 'alto': 1}\n\n"
        "def score(item):\n"
        "    prioridad = item.get('prioridad', '').lower()\n"
        "    presupuesto = item.get('presupuesto', '').lower()\n"
        "    return PRIORITY_SCORE.get(prioridad, 0) + BUDGET_SCORE.get(presupuesto, 0)\n\n"
        "def main():\n"
        "    if not INPUT.exists():\n"
        "        OUTPUT.write_text(json.dumps({'error': 'missing_validation_report'}, indent=2, ensure_ascii=False) + '\\n')\n"
        "        return\n"
        "    data = json.loads(INPUT.read_text())\n"
        "    valid = data.get('valid', [])\n"
        "    ranked = []\n"
        "    for item in valid:\n"
        "        enriched = dict(item)\n"
        "        enriched['score'] = score(item)\n"
        "        ranked.append(enriched)\n"
        "    ranked.sort(key=lambda x: (-x.get('score', 0), x.get('destino', '')))\n"
        "    OUTPUT.write_text(json.dumps({'ranked': ranked}, indent=2, ensure_ascii=False) + '\\n')\n\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )
    return True


def _run_python_script(script_path: Path) -> tuple[bool, str]:
    if not script_path.exists():
        return False, f"missing script: {script_path.as_posix()}"
    try:
        result = subprocess.run(
            [sys.executable, script_path.as_posix()],
            capture_output=True,
            text=True,
            check=False,
        )
        ok = result.returncode == 0
        output = (result.stdout or result.stderr or "").strip()
        return ok, output
    except Exception as exc:
        return False, str(exc)


def realize_task(task: dict) -> bool:
    task_id = task.get("id", "")
    title = task.get("title", "")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    if task_id == "task-deliverable-1":
        created = _ensure_input_file()
        _write(
            REPORT,
            "# Task Realization Report\n\n"
            "- Realized task-deliverable-1\n"
            f"- Created input file: {created}\n"
            f"- Ensured: {INPUT_FILE.as_posix()}\n"
        )
        return True

    if task_id == "task-deliverable-2":
        input_created = _ensure_input_file()
        parser_created = _ensure_parser_file()
        parser_ok, parser_output = _run_python_script(PARSER_FILE)
        _write(
            REPORT,
            "# Task Realization Report\n\n"
            "- Realized task-deliverable-2\n"
            f"- Prerequisite input ensured: {INPUT_FILE.as_posix()}\n"
            f"- Input created during this run: {input_created}\n"
            f"- Parser created during this run: {parser_created}\n"
            f"- Parser executed successfully: {parser_ok}\n"
            f"- Ensured parser: {PARSER_FILE.as_posix()}\n"
            f"- Ensured parsed JSON: {JSON_FILE.as_posix()}\n"
            f"- Parser output: {parser_output or 'no console output'}\n"
        )
        return parser_ok

    if task_id == "task-deliverable-3":
        input_created = _ensure_input_file()
        parser_created = _ensure_parser_file()
        validator_created = _ensure_validator_file()
        parser_ok, parser_output = _run_python_script(PARSER_FILE)
        validator_ok, validator_output = _run_python_script(VALIDATOR_FILE)
        _write(
            REPORT,
            "# Task Realization Report\n\n"
            "- Realized task-deliverable-3\n"
            f"- Ensured input: {INPUT_FILE.as_posix()}\n"
            f"- Input created during this run: {input_created}\n"
            f"- Ensured parser: {PARSER_FILE.as_posix()}\n"
            f"- Parser created during this run: {parser_created}\n"
            f"- Parser executed successfully: {parser_ok}\n"
            f"- Ensured JSON data file: {JSON_FILE.as_posix()}\n"
            f"- Ensured validator: {VALIDATOR_FILE.as_posix()}\n"
            f"- Validator created during this run: {validator_created}\n"
            f"- Validator executed successfully: {validator_ok}\n"
            f"- Ensured validation report: {VALIDATION_REPORT.as_posix()}\n"
            f"- Parser output: {parser_output or 'no console output'}\n"
            f"- Validator output: {validator_output or 'no console output'}\n"
        )
        return parser_ok and validator_ok

    if task_id == "task-deliverable-4":
        input_created = _ensure_input_file()
        parser_created = _ensure_parser_file()
        validator_created = _ensure_validator_file()
        prioritizer_created = _ensure_prioritizer_file()
        parser_ok, parser_output = _run_python_script(PARSER_FILE)
        validator_ok, validator_output = _run_python_script(VALIDATOR_FILE)
        prioritizer_ok, prioritizer_output = _run_python_script(PRIORITIZER_FILE)
        _write(
            REPORT,
            "# Task Realization Report\n\n"
            "- Realized task-deliverable-4\n"
            f"- Ensured input: {INPUT_FILE.as_posix()}\n"
            f"- Input created during this run: {input_created}\n"
            f"- Parser created during this run: {parser_created}\n"
            f"- Validator created during this run: {validator_created}\n"
            f"- Prioritizer created during this run: {prioritizer_created}\n"
            f"- Parser executed successfully: {parser_ok}\n"
            f"- Validator executed successfully: {validator_ok}\n"
            f"- Prioritizer executed successfully: {prioritizer_ok}\n"
            f"- Ensured prioritizer: {PRIORITIZER_FILE.as_posix()}\n"
            f"- Ensured ranking file: {RANKING_FILE.as_posix()}\n"
            f"- Parser output: {parser_output or 'no console output'}\n"
            f"- Validator output: {validator_output or 'no console output'}\n"
            f"- Prioritizer output: {prioritizer_output or 'no console output'}\n"
        )
        return parser_ok and validator_ok and prioritizer_ok and RANKING_FILE.exists()

    _write(
        REPORT,
        "# Task Realization Report\n\n"
        f"- No concrete artifact realization rule for task: {task_id} ({title})\n"
    )
    return False


if __name__ == "__main__":
    print(realize_task({"id": "task-deliverable-4", "title": "Implementar entregable 4"}))
