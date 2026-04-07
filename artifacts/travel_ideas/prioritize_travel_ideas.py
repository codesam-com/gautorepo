from pathlib import Path
import json

INPUT = Path('artifacts/travel_ideas/validation_report.json')
OUTPUT = Path('artifacts/travel_ideas/prioritized_travel_ideas.json')

PRIORITY_SCORE = {'alta': 3, 'media': 2, 'baja': 1}
BUDGET_SCORE = {'bajo': 3, 'medio': 2, 'alto': 1}

def score(item):
    prioridad = item.get('prioridad', '').lower()
    presupuesto = item.get('presupuesto', '').lower()
    return PRIORITY_SCORE.get(prioridad, 0) + BUDGET_SCORE.get(presupuesto, 0)

def main():
    if not INPUT.exists():
        OUTPUT.write_text(json.dumps({'error': 'missing_validation_report'}, indent=2, ensure_ascii=False) + '\n')
        return
    data = json.loads(INPUT.read_text())
    valid = data.get('valid', [])
    ranked = []
    for item in valid:
        enriched = dict(item)
        enriched['score'] = score(item)
        ranked.append(enriched)
    ranked.sort(key=lambda x: (-x.get('score', 0), x.get('destino', '')))
    OUTPUT.write_text(json.dumps({'ranked': ranked}, indent=2, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    main()
