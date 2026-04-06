import hashlib
import json
from pathlib import Path

GOAL_FILE = Path("user/goal.md")
HASH_FILE = Path("state/instruction_hash.txt")


def compute_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


def read_goal():
    if not GOAL_FILE.exists():
        return ""
    return GOAL_FILE.read_text()


def read_previous_hash():
    if not HASH_FILE.exists():
        return ""
    return HASH_FILE.read_text().strip()


def write_hash(h):
    HASH_FILE.write_text(h)


def detect_change():
    goal = read_goal()
    current_hash = compute_hash(goal)
    previous_hash = read_previous_hash()

    if current_hash != previous_hash:
        write_hash(current_hash)
        return True, goal

    return False, goal


if __name__ == "__main__":
    changed, goal = detect_change()

    if changed:
        print("Goal changed. Replanning required.")
    else:
        print("No change in goal.")
