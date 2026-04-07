from pathlib import Path
import json

INPUT = Path('artifacts/travel_ideas/travel_ideas_input.md')
OUTPUT = Path('artifacts/travel_ideas/travel_ideas.json')

def parse_line(line: str):
    raw = line.strip().lstrip('-').strip()
    parts = [p.strip() for p in raw.split('|')]
    item = {}
    for part in parts:
        if ':' in part:
            k, v = part.split(':', 1)
            item[k.strip()] = v.strip()
    return item

def main():
    entries = []
    if INPUT.exists():
        for line in INPUT.read_text().splitlines():
            if line.strip().startswith('- '):
                entries.append(parse_line(line))
    OUTPUT.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    main()
