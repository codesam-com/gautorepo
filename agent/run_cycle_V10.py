from run_cycle import main as previous_cycle
from goal_interpreter import interpret_goal
from self_improver import analyze_self


def main():
    print("Running base autonomous cycle...")
    previous_cycle()

    print("Interpreting goal semantically...")
    interpretation = interpret_goal()
    print(f"Primary goal: {interpretation.get('primary_goal')}")

    print("Running self improvement analysis...")
    improvements = analyze_self()
    for item in improvements:
        print(f"Improvement insight: {item}")


if __name__ == "__main__":
    main()
