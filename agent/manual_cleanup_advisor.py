from pathlib import Path

REPORT = Path("reports/manual_cleanup_requests.md")


def generate_cleanup_requests():
    requests = []

    legacy_candidates = [
        ".github/workflows/orchestrator_v2.yml",
        ".github/workflows/orchestrator_main.yml",
    ]

    for candidate in legacy_candidates:
        if Path(candidate).exists():
            requests.append(f"- Eliminar: {candidate}")

    if not requests:
        requests.append("- No cleanup actions requested at this time")

    REPORT.write_text("# Manual Cleanup Requests\n\n" + "\n".join(requests) + "\n")
    return requests


if __name__ == "__main__":
    generate_cleanup_requests()
