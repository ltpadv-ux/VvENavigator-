"""Evidence-based governance and closure for VvE Navigator improvement backlog."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION = "4.9.0"


def govern_improvement_closure(
    backlog: dict[str, Any],
    history: list[dict[str, Any]],
    sla: dict[str, Any],
    improvement: dict[str, Any],
    required_stable_runs: int = 3,
) -> dict[str, Any]:
    """Close backlog items only when objective production evidence supports closure."""
    items = [dict(x) for x in backlog.get("items", []) or []]
    active_checks = {str(x.get("check", "")) for x in improvement.get("root_causes", []) or []}
    recent = history[-max(1, required_stable_runs):]
    stable_runs = len(recent) >= required_stable_runs and all(
        str(x.get("control_status", "")) in {"GROEN", "HERSTELD"} and int(x.get("blocker_count", 0) or 0) == 0
        for x in recent
    )
    sla_ok = bool(sla.get("compliant", False))
    reliability = float(sla.get("release_reliability_score", 0.0) or 0.0)
    minimum = float(sla.get("minimum_reliability", 95.0) or 95.0)
    now = datetime.now(timezone.utc).isoformat()
    decisions: list[dict[str, Any]] = []

    for item in items:
        check = str(item.get("check", ""))
        already_closed = str(item.get("status", "")).upper() in {"GEREED", "DONE", "CLOSED"}
        cause_absent = check not in active_checks
        evidence = {
            "sla_compliant": sla_ok,
            "reliability_at_or_above_target": reliability >= minimum,
            "stable_production_runs": stable_runs,
            "required_stable_runs": required_stable_runs,
            "root_cause_not_recurred": cause_absent,
        }
        eligible = all(v for k, v in evidence.items() if k != "required_stable_runs")
        if eligible and not already_closed:
            item["status"] = "GEREED"
            item["progress_percent"] = 100
            item["closed_at"] = now
            item["closure_reason"] = f"Effect bewezen: SLA >= {minimum:.1f}%, {required_stable_runs} stabiele productieruns en oorzaak niet teruggekomen."
            decision = "CLOSED"
        elif already_closed:
            decision = "ALREADY_CLOSED"
        else:
            decision = "KEEP_OPEN"
        item["governance_evidence"] = evidence
        item["updated_at"] = now
        decisions.append({"id": item.get("id", ""), "decision": decision, "evidence": evidence})

    open_items = [x for x in items if str(x.get("status", "OPEN")).upper() not in {"GEREED", "DONE", "CLOSED"}]
    closed_items = [x for x in items if str(x.get("status", "")).upper() in {"GEREED", "DONE", "CLOSED"}]
    return {
        "improvement_governance_version": ENGINE_VERSION,
        "status": "ALL_CLOSED" if items and not open_items else "GOVERNED",
        "items": items,
        "open_count": len(open_items),
        "closed_count": len(closed_items),
        "closure_decisions": decisions,
        "stable_run_requirement": required_stable_runs,
        "next_action": "Geen open verbeteritems" if not open_items else open_items[0].get("recommended_action", "Werk het hoogste prioriteitsitem verder af."),
    }
