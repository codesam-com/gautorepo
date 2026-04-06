from pathlib import Path

REPORT = Path("reports/self_improvement.md")


def analyze_self():
    findings = []

    # simple heuristic checks
    if not Path("agent/generated_tools").exists():
        findings.append("No generated tools directory detected")

    if not Path("reports/task_evaluation.md").exists():
        findings.append("Task evaluation report missing")

    if not findings:
        findings.append("No immediate structural improvements detected")

    REPORT.write_text(
        "# Self Improvement Analysis\n\n" + "\n".join(f"- {f}" for f in findings) + "\n"
    )

    return findings


if __name__ == "__main__":
    analyze_self()
