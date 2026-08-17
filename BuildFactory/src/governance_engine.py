"""Governance and ALV workflow engine for VvE Navigator."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass(frozen=True)
class ALVProposal:
    agenda_item: str
    decision_text: str
    financial_impact: float
    owner: str
    status: str
    priority: str
    horizon: str
    rationale: str


def status_from_priority(priority: str) -> str:
    mapping = {
        "NU": "BESLUIT NODIG",
        "HOOG": "VOORBEREIDEN",
        "PLANNEN": "AGENDEREN",
        "MONITOREN": "VOLGEN",
    }
    return mapping.get(priority.upper(), "AGENDEREN")


def proposal_from_decision(
    decision: dict,
    financial_impact: float = 0.0,
    owner: str = "Bestuur",
) -> ALVProposal:
    """Translate one Decision Engine result into an ALV-ready proposal."""
    action = str(decision.get("action", "Besluitvoorstel"))
    priority = str(decision.get("priority", "PLANNEN")).upper()
    horizon = str(decision.get("horizon", "2-5 jaar"))
    rationale = str(decision.get("rationale", ""))
    component = action.split(":", 1)[0].strip() if ":" in action else action
    agenda_item = f"Besluit {component}"
    decision_text = (
        f"De ALV besluit het bestuur mandaat te geven om '{action}' uit te werken en uit te voeren "
        f"binnen de vastgestelde financiële kaders."
    )
    return ALVProposal(
        agenda_item=agenda_item,
        decision_text=decision_text,
        financial_impact=round(float(financial_impact), 2),
        owner=owner,
        status=status_from_priority(priority),
        priority=priority,
        horizon=horizon,
        rationale=rationale,
    )


def build_alv_agenda(
    decisions: Iterable[dict],
    financial_impacts: dict[str, float] | None = None,
    owner: str = "Bestuur",
) -> list[dict]:
    """Build an ordered ALV agenda from ranked board decisions."""
    impacts = financial_impacts or {}
    proposals: list[ALVProposal] = []
    for decision in decisions:
        action = str(decision.get("action", ""))
        component = action.split(":", 1)[0].strip() if ":" in action else action
        proposals.append(
            proposal_from_decision(decision, impacts.get(component, 0.0), owner)
        )
    return [asdict(item) for item in proposals]


def governance_summary(agenda: Iterable[dict]) -> dict:
    """Return governance KPIs for the board cockpit."""
    rows = list(agenda)
    return {
        "agenda_items": len(rows),
        "decision_needed": sum(1 for row in rows if row.get("status") == "BESLUIT NODIG"),
        "prepare": sum(1 for row in rows if row.get("status") == "VOORBEREIDEN"),
        "planned": sum(1 for row in rows if row.get("status") == "AGENDEREN"),
        "monitor": sum(1 for row in rows if row.get("status") == "VOLGEN"),
        "total_financial_impact": round(sum(float(row.get("financial_impact", 0.0)) for row in rows), 2),
    }
