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
FINAL_REPORT = ARTIFACT_DIR / "final_report.md"


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
        result = subprocess.run([sys.executable, script_path.as_posix()], capture_output=True, text=True, check=False)
        ok = result.returncode == 0
        output = (result.stdout or result.stderr or "").strip()
        return ok, output
    except Exception as exc:
        return False, str(exc)


def _ensure_pipeline_ready() -> dict:
    input_created = _ensure_input_file()
    parser_created = _ensure_parser_file()
    validator_created = _ensure_validator_file()
    prioritizer_created = _ensure_prioritizer_file()
    parser_ok, parser_output = _run_python_script(PARSER_FILE)
    validator_ok, validator_output = _run_python_script(VALIDATOR_FILE)
    prioritizer_ok, prioritizer_output = _run_python_script(PRIORITIZER_FILE)
    return {
        "input_created": input_created,
        "parser_created": parser_created,
        "validator_created": validator_created,
        "prioritizer_created": prioritizer_created,
        "parser_ok": parser_ok,
        "validator_ok": validator_ok,
        "prioritizer_ok": prioritizer_ok,
        "parser_output": parser_output,
        "validator_output": validator_output,
        "prioritizer_output": prioritizer_output,
    }


def _build_final_report() -> bool:
    if not VALIDATION_REPORT.exists() or not RANKING_FILE.exists():
        return False
    validation = json.loads(VALIDATION_REPORT.read_text())
    ranking = json.loads(RANKING_FILE.read_text())
    valid = validation.get("valid", [])
    invalid = validation.get("invalid", [])
    ranked = ranking.get("ranked", [])

    lines = [
        "# Informe final de ideas de viaje",
        "",
        "## Ideas válidas",
    ]
    if valid:
        for item in valid:
            lines.append(f"- {item.get('destino', 'Sin destino')} | presupuesto: {item.get('presupuesto', '')} | duracion: {item.get('duracion', '')} | prioridad: {item.get('prioridad', '')}")
    else:
        lines.append("- No hay ideas válidas")

    lines.extend(["", "## Ideas inválidas"])
    if invalid:
        for item in invalid:
            original = item.get("item", {})
            missing = ", ".join(item.get("missing", []))
            lines.append(f"- {original.get('destino', 'Sin destino')} | campos faltantes: {missing}")
    else:
        lines.append("- No hay ideas inválidas")

    lines.extend(["", "## Ranking final"])
    if ranked:
        for idx, item in enumerate(ranked, start=1):
            lines.append(f"{idx}. {item.get('destino', 'Sin destino')} — score {item.get('score', 0)}")
    else:
        lines.append("- No hay ranking disponible")

    lines.extend(["", "## Explicación del ranking"])
    lines.append("- La puntuación suma prioridad personal y presupuesto preferente.")
    lines.append("- Mayor prioridad personal aporta más puntos.")
    lines.append("- Presupuestos más bajos reciben mejor puntuación.")
    lines.append("- Solo las ideas válidas entran en el ranking final.")
    lines.append("")

    _write(FINAL_REPORT, "\n".join(lines))
    return True


def realize_task(task: dict) -> bool:
    task_id = task.get("id", "")
    title = task.get("title", "")
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    if task_id == "task-deliverable-5":
        status = _ensure_pipeline_ready()
        report_ok = _build_final_report()
        _write(
            REPORT,
            "# Task Realization Report\n\n"
            "- Realized task-deliverable-5\n"
            f"- Parser executed successfully: {status['parser_ok']}\n"
            f"- Validator executed successfully: {status['validator_ok']}\n"
            f"- Prioritizer executed successfully: {status['prioritizer_ok']}\n"
            f"- Final report created: {report_ok}\n"
            f"- Ensured final report: {FINAL_REPORT.as_posix()}\n"
            f"- Parser output: {status['parser_output'] or 'no console output'}\n"
            f"- Validator output: {status['validator_output'] or 'no console output'}\n"
            f"- Prioritizer output: {status['prioritizer_output'] or 'no console output'}\n"
        )
        return status['parser_ok'] and status['validator_ok'] and status['prioritizer_ok'] and report_ok

    _write(
        REPORT,
        "# Task Realization Report\n\n"
        f"- No concrete artifact realization rule for task: {task_id} ({title})\n"
    )
    return False


if __name__ == "__main__":
    print(realize_task({"id": "task-deliverable-5", "title": "Implementar entregable 5"}))
