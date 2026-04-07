from pathlib import Path
import json

INPUT = Path('artifacts/travel_ideas/travel_ideas.json')
OUTPUT = Path('artifacts/travel_ideas/validation_report.json')

REQUIRED = ['destino', 'presupuesto', 'duracion', 'prioridad']

def main():
    if not INPUT.exists():
        OUTPUT.write_text(json.dumps({'error': 'missing_input'}, indent=2, ensure_ascii=False) + '\n')
        return
    data = json.loads(INPUT.read_text())
    valid = []
    invalid = []
    for item in data:
        missing = [k for k in REQUIRED if not item.get(k)]
        if missing:
            invalid.append({'item': item, 'missing': missing})
        else:
            valid.append(item)
    OUTPUT.write_text(json.dumps({'valid': valid, 'invalid': invalid}, indent=2, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    main()
