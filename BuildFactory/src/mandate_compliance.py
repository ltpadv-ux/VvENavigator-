"""Compliance, budget and deadline control for ALV execution mandates."""
from __future__ import annotations
from datetime import date, datetime, timezone
from typing import Any

ENGINE_VERSION = "5.4.0"


def evaluate_mandate_compliance(mandates: dict[str, Any], today: date | None = None) -> dict[str, Any]:
    today = today or date.today()
    findings: list[dict[str, Any]] = []
    reviewed = []
    for mandate in mandates.get("mandates", []) or []:
        item = dict(mandate)
        budget = float(item.get("budget", 0.0) or 0.0)
        spent = float(item.get("spent_amount", 0.0) or 0.0)
        status = str(item.get("status", "OPEN")).upper()
        issues: list[str] = []
        severity = "GROEN"

        if budget > 0 and spent > budget:
            issues.append(f"Budget overschreden met EUR {spent-budget:.2f}")
            severity = "ROOD"
        elif budget > 0 and spent >= budget * 0.9 and status not in {"GEREED", "AFGEROND", "CLOSED"}:
            issues.append("Budgetverbruik is 90% of hoger terwijl mandaat nog open staat")
            severity = "ORANJE"

        deadline = str(item.get("deadline", "") or "")
        if deadline:
            try:
                due = date.fromisoformat(deadline[:10])
                if due < today and status not in {"GEREED", "AFGEROND", "CLOSED"}:
                    issues.append(f"Deadline verstreken op {due.isoformat()}")
                    severity = "ROOD"
            except ValueError:
                issues.append("Ongeldige deadline-notatie; verwacht YYYY-MM-DD")
                severity = "ORANJE" if severity != "ROOD" else severity

        if not str(item.get("owner", "")).strip():
            issues.append("Geen mandaat-eigenaar vastgelegd")
            severity = "ORANJE" if severity == "GROEN" else severity
        if not str(item.get("mandate_text", "")).strip():
            issues.append("Geen uitvoeringskader vastgelegd")
            severity = "ROOD"

        remaining = round(budget - spent, 2)
        item["compliance_status"] = severity
        item["budget_remaining"] = remaining
        item["compliance_issues"] = issues
        reviewed.append(item)
        if issues:
            findings.append({
                "mandate_id": item.get("mandate_id", ""),
                "decision_id": item.get("decision_id", ""),
                "owner": item.get("owner", ""),
                "severity": severity,
                "issues": issues,
                "escalation": "BESTUURLIJKE ESCALATIE" if severity == "ROOD" else "BEHEERACTIE",
            })

    red = sum(1 for x in findings if x["severity"] == "ROOD")
    orange = sum(1 for x in findings if x["severity"] == "ORANJE")
    return {
        "mandate_compliance_version": ENGINE_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "GEBLOKKEERD" if red else "AANDACHT" if orange else "BINNEN MANDAAT",
        "mandate_count": len(reviewed),
        "red_count": red,
        "orange_count": orange,
        "findings": findings,
        "mandates": reviewed,
        "human_escalation_required": red > 0,
        "next_action": findings[0]["issues"][0] if findings else "Geen afwijking: uitvoering blijft binnen ALV-mandaat.",
    }
