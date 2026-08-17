"""Release Control Center for VvE Navigator production runs."""
from __future__ import annotations
from typing import Any

CONTROL_CENTER_VERSION = "4.4.0"


def build_release_control_center(report: dict[str, Any]) -> dict[str, Any]:
    verification = report.get("verification", {}) or {}
    diagnostics = report.get("diagnostics", {}) or {}
    healing = report.get("self_healing", {}) or {}

    verified = bool(verification.get("verified", False))
    healing_status = str(healing.get("status", "NOT_RUN")).upper()

    if verified and healing_status in {"NOT_RUN", "NOT_NEEDED"}:
        status = "GROEN"
    elif healing_status == "HEALED" and bool((healing.get("after") or {}).get("verified", False)):
        status = "HERSTELD"
    else:
        status = "GEBLOKKEERD"

    repairs = healing.get("repairs", []) or []
    human_actions = healing.get("human_actions", []) or []
    if not human_actions:
        human_actions = diagnostics.get("diagnostics", []) or [] if status == "GEBLOKKEERD" else []

    return {
        "release_control_center_version": CONTROL_CENTER_VERSION,
        "status": status,
        "release_status": (report.get("release", {}) or {}).get("status", ""),
        "verification_status": verification.get("status", ""),
        "self_healing_status": healing_status,
        "repairs_executed": repairs,
        "repair_count": len(repairs),
        "human_actions": human_actions,
        "human_action_count": len(human_actions),
        "next_action": (
            "Geen actie nodig"
            if status == "GROEN"
            else "Controleer herstelde release en archiveer het verificatierapport"
            if status == "HERSTELD"
            else (human_actions[0].get("remediation", "Menselijke beoordeling vereist") if human_actions else "Menselijke beoordeling vereist")
        ),
    }
