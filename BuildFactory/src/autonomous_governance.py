"""Autonomous governance cycle with explicit human decision gates."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION = "5.0.0"


def build_governance_cycle(report: dict[str, Any]) -> dict[str, Any]:
    control = report.get("control_center", {}) or {}
    sla = report.get("reliability_sla", {}) or {}
    governance = report.get("improvement_governance", {}) or {}
    diagnostics = report.get("diagnostics", {}) or {}
    status = str(control.get("status", "GEBLOKKEERD"))
    blockers = int(diagnostics.get("blocking_count", diagnostics.get("blocker_count", 0)) or 0)
    open_improvements = int(governance.get("open_count", 0) or 0)
    sla_ok = bool(sla.get("compliant", False))

    human_gates = []
    if status == "GEBLOKKEERD" or blockers:
        human_gates.append({"gate":"RELEASE_EXCEPTION","owner":"Bestuur / Beheerder","decision":"BEOORDELEN","reason":"Productierelease bevat blokkades."})
    if not sla_ok:
        human_gates.append({"gate":"SLA_EXCEPTION","owner":"Product owner","decision":"BEOORDELEN","reason":"Releasebetrouwbaarheid voldoet niet aan SLA."})
    if open_improvements:
        human_gates.append({"gate":"IMPROVEMENT_OVERSIGHT","owner":"Bestuur / Beheerder","decision":"VOLGEN","reason":f"{open_improvements} verbeteritem(s) staan nog open."})

    autonomous_ok = status in {"GROEN","HERSTELD"} and sla_ok and not human_gates
    return {
        "autonomous_governance_version": ENGINE_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cycle_status": "AUTONOOM GROEN" if autonomous_ok else "MENSELIJK BESLUIT VEREIST",
        "release_status": status,
        "sla_compliant": sla_ok,
        "open_improvements": open_improvements,
        "human_decision_gates": human_gates,
        "audit_trail": [
            {"stage":"Release Control Center","result":status},
            {"stage":"Reliability SLA","result":"BINNEN SLA" if sla_ok else "SLA BREACH"},
            {"stage":"Improvement Governance","result":governance.get("status","ONBEKEND")},
        ],
        "next_action": "Releasecyclus kan zonder uitzondering worden afgerond." if autonomous_ok else human_gates[0]["reason"],
    }
