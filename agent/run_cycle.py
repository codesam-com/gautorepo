from run_cycle import main as previous_cycle
from toolmaker import create_tool_if_needed


def main():
    print("Running base autonomous cycle...")
    previous_cycle()

    print("Evaluating need for new tools...")

    # simple heuristic: always ensure at least one helper exists
    created, path = create_tool_if_needed(
        tool_name="basic_analysis_tool",
        purpose="Provide basic structured analysis capability"
    )

    if created:
        print(f"New tool created at: {path}")
    else:
        print("Required tool already exists")


if __name__ == "__main__":
    main()
