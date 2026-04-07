from pathlib import Path
import json

ARTIFACT_DIR = Path("artifacts/travel_ideas")
REPORT = Path("reports/task_realization_report.md")


def _write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def realize_task(task: dict) -> bool:
    task_id = task.get("id", "")
    title = task.get("title", "")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    if task_id == "task-deliverable-1":
        _write(
            ARTIFACT_DIR / "travel_ideas_input.md",
            "# Ideas de viaje\n\n"
            "- destino: Lisboa | presupuesto: bajo | duracion: 3 dias | prioridad: alta\n"
            "- destino: Tokio | presupuesto: alto | duracion: 10 dias | prioridad: media\n"
            "- destino: Sin destino | presupuesto: | duracion: | prioridad: baja\n"
            "- destino: Escapada rural | presupuesto: medio | duracion: 2 dias | prioridad: alta\n"
        )
        _write(
            REPORT,
            "# Task Realization Report\n\n"
            "- Realized task-deliverable-1\n"
            "- Created: artifacts/travel_ideas/travel_ideas_input.md\n"
        )
        return True

    if task_id == "task-deliverable-2":
        _write(
            ARTIFACT_DIR / "parse_travel_ideas.py",
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
        _write(
            REPORT,
            "# Task Realization Report\n\n"
            "- Realized task-deliverable-2\n"
            "- Created: artifacts/travel_ideas/parse_travel_ideas.py\n"
        )
        return True

    if task_id == "task-deliverable-3":
        _write(
            ARTIFACT_DIR / "validate_travel_ideas.py",
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
        _write(
            REPORT,
            "# Task Realization Report\n\n"
            "- Realized task-deliverable-3\n"
            "- Created: artifacts/travel_ideas/validate_travel_ideas.py\n"
        )
        return True

    _write(
        REPORT,
        "# Task Realization Report\n\n"
        f"- No concrete artifact realization rule for task: {task_id} ({title})\n"
    )
    return False


if __name__ == "__main__":
    print(realize_task({"id": "task-deliverable-1", "title": "Implementar entregable 1"}))
