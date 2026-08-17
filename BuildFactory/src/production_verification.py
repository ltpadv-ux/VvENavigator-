"""Production verification for end-to-end VvE Navigator releases."""
from __future__ import annotations
from pathlib import Path
from typing import Any

VERIFICATION_VERSION = "4.1.0"
REQUIRED_ARTIFACTS = ("pdf", "docx", "xlsx")


def verify_production_result(result: dict[str, Any]) -> dict[str, Any]:
    """Verify a completed production release without trusting status labels alone."""
    issues: list[str] = []
    checks: dict[str, bool] = {}

    checks["released_for_alv"] = result.get("status") == "VRIJGEGEVEN VOOR ALV"
    if not checks["released_for_alv"]:
        issues.append(f"Onverwachte release-status: {result.get('status', 'ONTBREKEND')}")

    native = result.get("native_export", {}) or {}
    files = native.get("files", {}) or {}
    for key in REQUIRED_ARTIFACTS:
        path = Path(str(files.get(key, "")))
        ok = bool(str(path)) and path.exists() and path.stat().st_size > 0
        checks[f"artifact_{key}"] = ok
        if not ok:
            issues.append(f"Artifact ontbreekt of is leeg: {key.upper()}")

    package = result.get("package", {}) or {}
    zip_path = Path(str(package.get("distribution_zip", "")))
    checks["distribution_zip"] = bool(str(zip_path)) and zip_path.exists() and zip_path.stat().st_size > 0
    if not checks["distribution_zip"]:
        issues.append("Distributie-ZIP ontbreekt of is leeg")

    validation = result.get("validation", {}) or {}
    checks["sign_off_go"] = validation.get("sign_off", {}).get("decision") == "GO"
    if not checks["sign_off_go"]:
        issues.append("Formele sign-off is geen GO")

    quality = result.get("enterprise", {}).get("release", {}).get("quality_gate", {}) or {}
    checks["quality_gate"] = bool(quality.get("can_publish", False))
    if not checks["quality_gate"]:
        issues.append("Quality Gate is niet publiceerbaar")

    verified = all(checks.values())
    return {
        "production_verification_version": VERIFICATION_VERSION,
        "status": "VERIFIED" if verified else "FAILED",
        "verified": verified,
        "checks": checks,
        "issues": issues,
    }
