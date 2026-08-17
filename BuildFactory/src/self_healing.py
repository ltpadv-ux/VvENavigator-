"""Safe self-healing for VvE Navigator production releases."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import zipfile

from binary_renderers import render_pdf, render_docx, render_xlsx
from release_packaging import write_release_package
from production_verification import verify_production_result
from verification_diagnostics import diagnose_verification

SELF_HEALING_VERSION = "4.3.0"
SAFE_CHECKS = {"artifact_pdf", "artifact_docx", "artifact_xlsx", "distribution_zip"}


def _safe_repair(check: str, result: dict[str, Any]) -> dict[str, Any]:
    model = result.get("render_model") or result.get("publication", {}).get("render_model")
    native = result.get("native_export", {}) or {}
    files = native.get("files", {}) or {}
    if check == "artifact_pdf" and model and files.get("pdf"):
        render_pdf(model, files["pdf"]); return {"check": check, "status": "REPAIRED", "action": "PDF opnieuw gerenderd"}
    if check == "artifact_docx" and model and files.get("docx"):
        render_docx(model, files["docx"]); return {"check": check, "status": "REPAIRED", "action": "DOCX opnieuw gerenderd"}
    if check == "artifact_xlsx" and model and files.get("xlsx"):
        render_xlsx(model, files["xlsx"]); return {"check": check, "status": "REPAIRED", "action": "XLSX opnieuw gerenderd"}
    if check == "distribution_zip":
        package = result.get("package", {}) or {}; output = Path(package.get("distribution_zip", "artifacts/release.zip")).parent
        version = str(result.get("orchestrator_version", "4.3.0")); name = str(result.get("release_index", {}).get("vve_name", "VvE Navigator"))
        write_release_package(version, name, {k:v for k,v in files.items() if k in {"html","pdf","docx","xlsx"}}, output)
        return {"check": check, "status": "REPAIRED", "action": "Distributiepakket opnieuw opgebouwd"}
    return {"check": check, "status": "SKIPPED", "action": "Geen veilige automatische reparatie beschikbaar"}


def run_self_healing(result: dict[str, Any], max_attempts: int = 1) -> dict[str, Any]:
    """Attempt only deterministic artifact/package repairs; never alter governance or source data."""
    before = verify_production_result(result)
    diagnostics = diagnose_verification(before, result)
    repairs: list[dict[str, Any]] = []
    if before.get("verified"):
        return {"self_healing_version": SELF_HEALING_VERSION, "status": "NOT_NEEDED", "before": before, "after": before, "repairs": [], "escalation_required": False}

    failed = [k for k,v in (before.get("checks", {}) or {}).items() if not v]
    for _ in range(max(0, max_attempts)):
        for check in failed:
            if check in SAFE_CHECKS:
                repairs.append(_safe_repair(check, result))
        break

    after = verify_production_result(result)
    remaining = diagnose_verification(after, result)
    human_only = [d for d in remaining.get("diagnostics", []) if d.get("check") not in SAFE_CHECKS]
    return {
        "self_healing_version": SELF_HEALING_VERSION,
        "status": "HEALED" if after.get("verified") else "ESCALATE",
        "before": before,
        "diagnostics_before": diagnostics,
        "repairs": repairs,
        "after": after,
        "diagnostics_after": remaining,
        "escalation_required": bool(not after.get("verified")),
        "human_actions": human_only,
    }
