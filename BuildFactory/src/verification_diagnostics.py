"""Failure diagnostics for VvE Navigator production verification."""
from __future__ import annotations
from typing import Any

DIAGNOSTICS_VERSION = "4.2.0"

REMEDIATIONS = {
    "released_for_alv": "Controleer de release-validation en herstel blokkerende sign-off voorwaarden.",
    "artifact_pdf": "Controleer ReportLab-rendering en het PDF-doelpad.",
    "artifact_docx": "Controleer python-docx-rendering en het DOCX-doelpad.",
    "artifact_xlsx": "Controleer openpyxl-rendering en het XLSX-doelpad.",
    "distribution_zip": "Controleer Release Packaging en of gegenereerde bestanden in het ZIP-pakket worden opgenomen.",
    "sign_off_go": "Controleer release_validation.py; alle verplichte outputs, checksums en Quality Gate moeten groen zijn.",
    "quality_gate": "Herstel de blokkerende Compliance & Quality-issues in brondata, MJOP, reserve of besluitvorming.",
}


def diagnose_verification(verification: dict[str, Any], production_result: dict[str, Any] | None = None) -> dict[str, Any]:
    """Translate failed verification checks into module-level diagnostics and recovery actions."""
    production_result = production_result or {}
    checks = verification.get("checks", {}) or {}
    diagnostics: list[dict[str, str]] = []
    for check, ok in checks.items():
        if ok:
            continue
        module = {
            "released_for_alv": "Release Validation & Sign-off",
            "artifact_pdf": "Production Binary Renderers / PDF",
            "artifact_docx": "Production Binary Renderers / DOCX",
            "artifact_xlsx": "Production Binary Renderers / XLSX",
            "distribution_zip": "Release Packaging & Distribution",
            "sign_off_go": "Release Validation & Sign-off",
            "quality_gate": "Compliance & Quality Engine",
        }.get(check, "Production Verification")
        diagnostics.append({"check": check, "module": module, "severity": "BLOCKER", "remediation": REMEDIATIONS.get(check, "Inspecteer de mislukte controle en herstel de bronoorzaak.")})

    quality = production_result.get("enterprise", {}).get("release", {}).get("quality_gate", {}) or {}
    for issue in quality.get("issues", []) or []:
        if isinstance(issue, dict):
            diagnostics.append({
                "check": str(issue.get("code", "quality_issue")),
                "module": "Compliance & Quality Engine",
                "severity": str(issue.get("severity", "BLOCKER")),
                "remediation": str(issue.get("message", "Herstel de Quality Gate-afwijking.")),
            })

    return {
        "verification_diagnostics_version": DIAGNOSTICS_VERSION,
        "status": "CLEAR" if not diagnostics else "ACTION_REQUIRED",
        "blocker_count": sum(1 for d in diagnostics if d["severity"].upper() == "BLOCKER"),
        "diagnostics": diagnostics,
        "next_action": "Geen herstelactie nodig" if not diagnostics else diagnostics[0]["remediation"],
    }
