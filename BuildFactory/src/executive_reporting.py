"""Executive reporting and ALV pack generator for VvE Navigator."""
from __future__ import annotations

from typing import Any


def _money(value: float) -> str:
    return f"€{value:,.0f}".replace(",", ".")


def build_executive_report(cockpit: dict[str, Any]) -> dict[str, Any]:
    """Create a board-ready executive report from the Executive Cockpit."""
    readiness = float(cockpit.get("decision_readiness", 0.0) or 0.0)
    reserve = float(cockpit.get("reserve", 0.0) or 0.0)
    deficit_probability = float(cockpit.get("deficit_probability", 0.0) or 0.0)
    monthly = float(cockpit.get("monthly_per_apartment", 0.0) or 0.0)
    strategy = str(cockpit.get("best_strategy", "Onbekend"))
    status = str(cockpit.get("status", "VOORBEREIDEN"))
    vni = float(cockpit.get("vni", 0.0) or 0.0)
    health = float(cockpit.get("health_score", 0.0) or 0.0)
    actions = list(cockpit.get("top_actions", []) or [])[:3]

    management_summary = (
        f"De VvE Navigator beoordeelt de besluitrijpheid op {readiness:.0f}/100 ({status}). "
        f"De voorkeursstrategie is {strategy}, met een geraamde tekortkans van {deficit_probability * 100:.1f}% "
        f"en een indicatieve bijdrage van €{monthly:.2f} per appartement per maand."
    )

    return {
        "report_type": "Executive Board Report",
        "title": "VvE Navigator - Bestuursrapport",
        "management_summary": management_summary,
        "kpis": {
            "decision_readiness": round(readiness, 2),
            "vni": round(vni, 2),
            "reserve": round(reserve, 2),
            "deficit_probability": round(deficit_probability, 4),
            "best_strategy": strategy,
            "monthly_per_apartment": round(monthly, 2),
            "health_score": round(health, 2),
        },
        "board_decision": cockpit.get("board_decision", ""),
        "top_actions": actions,
    }


def build_alv_decision_page(cockpit: dict[str, Any]) -> dict[str, Any]:
    """Create a concise ALV decision page from the Executive Cockpit."""
    strategy = str(cockpit.get("best_strategy", "Onbekend"))
    monthly = float(cockpit.get("monthly_per_apartment", 0.0) or 0.0)
    reserve = float(cockpit.get("reserve", 0.0) or 0.0)
    probability = float(cockpit.get("deficit_probability", 0.0) or 0.0)
    decision = str(cockpit.get("board_decision", ""))

    proposal = decision or (
        f"De ALV besluit de voorkeursstrategie {strategy} als uitgangspunt vast te stellen en de financiële "
        f"vertaling daarvan op te nemen in begroting en MJOP."
    )
    financial_consequence = (
        f"Indicatieve maandbijdrage: €{monthly:.2f} per appartement; geprojecteerde reserve: {_money(reserve)}; "
        f"geraamde kans op tekort: {probability * 100:.1f}%."
    )

    return {
        "document_type": "ALV Besluitpagina",
        "agenda_title": f"Besluit voorkeursstrategie {strategy}",
        "proposal": proposal,
        "financial_consequence": financial_consequence,
        "requested_decision": "Vaststellen / Aanpassen / Aanhouden",
        "follow_up": list(cockpit.get("top_actions", []) or [])[:3],
    }


def build_executive_pack(cockpit: dict[str, Any]) -> dict[str, Any]:
    """Return the complete executive reporting package from one source."""
    board_report = build_executive_report(cockpit)
    alv_page = build_alv_decision_page(cockpit)
    return {
        "pack_version": "3.2.0",
        "status": "GEREED" if cockpit else "ONVOLLEDIG",
        "executive_summary": board_report["management_summary"],
        "board_report": board_report,
        "alv_decision_page": alv_page,
        "source": "Executive Cockpit",
    }
