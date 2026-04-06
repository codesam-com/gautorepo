from pathlib import Path

REPORT = Path("reports/repo_hygiene.txt")
LEGACY_WORKFLOWS = [
    ".github/workflows/orchestrator.yml",
    ".github/workflows/orchestrator_v2.yml",
]
CANONICAL_WORKFLOW = ".github/workflows/orchestrator_main.yml"


def inspect_repo_hygiene():
    findings = []
    findings.append("REPO HYGIENE REPORT")
    findings.append(f"Canonical orchestrator: {CANONICAL_WORKFLOW}")

    for workflow in LEGACY_WORKFLOWS:
        path = Path(workflow)
        if path.exists():
            findings.append(f"LEGACY_WORKFLOW_PRESENT: {workflow}")
        else:
            findings.append(f"LEGACY_WORKFLOW_ABSENT: {workflow}")

    findings.append("Recommended action: keep orchestrator_main as the protected canonical workflow and remove legacy orchestrators when deletion tooling is enabled.")
    REPORT.write_text("\n".join(findings) + "\n")
    return findings


if __name__ == "__main__":
    inspect_repo_hygiene()
