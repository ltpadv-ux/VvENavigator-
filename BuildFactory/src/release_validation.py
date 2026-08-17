"""Release validation and formal sign-off for VvE Navigator."""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
from typing import Any

ENGINE_VERSION = "3.9.0"
REQUIRED_OUTPUTS = ("pdf", "docx", "xlsx")


def _checksum(path: str | Path) -> str:
    p = Path(path)
    h = sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def validate_release(
    release_index: dict[str, Any],
    quality_gate: dict[str, Any] | None = None,
    required_outputs: tuple[str, ...] = REQUIRED_OUTPUTS,
) -> dict[str, Any]:
    """Validate presence, integrity, quality gate and board-pack completeness."""
    quality_gate = quality_gate or {}
    files = release_index.get("files", []) or []
    by_name = {str(item.get("name", "")).lower(): item for item in files}
    issues: list[str] = []
    checks: dict[str, bool] = {}

    for output in required_outputs:
        item = by_name.get(output.lower())
        ok = bool(item and Path(str(item.get("path", ""))).exists())
        checks[f"required_{output}"] = ok
        if not ok:
            issues.append(f"Vereist bestand ontbreekt: {output.upper()}")

    integrity_ok = True
    for item in files:
        path = Path(str(item.get("path", "")))
        expected = str(item.get("sha256", ""))
        actual_ok = path.exists() and expected and _checksum(path) == expected
        integrity_ok = integrity_ok and bool(actual_ok)
        if not actual_ok:
            issues.append(f"Checksum ongeldig: {path.name or item.get('name','onbekend')}")
    checks["checksums"] = integrity_ok

    gate_status = str(quality_gate.get("status", "GOEDGEKEURD")).upper()
    can_publish = quality_gate.get("can_publish", True)
    gate_ok = gate_status != "BLOKKEREN" and bool(can_publish)
    checks["quality_gate"] = gate_ok
    if not gate_ok:
        issues.append("Quality Gate blokkeert publicatie")

    board_pack_ok = all(checks.get(f"required_{name}", False) for name in required_outputs)
    checks["board_pack_complete"] = board_pack_ok

    approved = all(checks.values())
    return {
        "release_validation_version": ENGINE_VERSION,
        "status": "VRIJGEGEVEN VOOR ALV" if approved else "NIET VRIJGEGEVEN",
        "approved": approved,
        "checks": checks,
        "issues": issues,
        "sign_off": {
            "decision": "GO" if approved else "NO-GO",
            "release_version": release_index.get("release_version", ""),
            "vve_name": release_index.get("vve_name", ""),
        },
    }
