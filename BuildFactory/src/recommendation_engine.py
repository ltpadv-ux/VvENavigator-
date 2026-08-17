"""Recommendation and explainability engine for VvE Navigator."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable, Any


@dataclass(frozen=True)
class Recommendation:
    title: str
    decision: str
    rationale: str
    financial_effect: str
    risk_effect: str
    sustainability_effect: str
    rejected_alternatives: list[str]
    confidence: str


def _money(value: float) -> str:
    return f"€{value:,.0f}".replace(",", ".")


def explain_strategy(
    optimization_result: dict[str, Any],
    apartments: int,
    alternatives: Iterable[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Translate an optimized strategy into board-ready reasoning."""
    best = dict(optimization_result.get("best_strategy") or {})
    if not best:
        return {
            "status": "GEEN ADVIES",
            "recommendation": {},
            "decision_summary": "Er is nog geen robuuste strategie gevonden.",
        }

    contribution = float(best.get("annual_contribution", 0.0))
    buffer = float(best.get("reserve_buffer", 0.0))
    probability = float(best.get("deficit_probability", 0.0))
    total_mjop = float(best.get("total_mjop", 0.0))
    sustainability = float(best.get("sustainability_score", 0.0))
    scenario = str(best.get("scenario", "Onbekend"))
    shift = int(best.get("shift_years", 0))
    monthly = contribution / max(apartments, 1) / 12

    rejected: list[str] = []
    for item in list(alternatives or optimization_result.get("top_strategies", []))[1:4]:
        rejected.append(
            f"{item.get('scenario', 'Alternatief')}: hogere doelkosten of een minder gunstige risico-/duurzaamheidsbalans"
        )

    if probability <= 0.05:
        risk_text = f"De geraamde kans op een tekort blijft beperkt tot {probability * 100:.1f}%."
        confidence = "HOOG"
    elif probability <= 0.10:
        risk_text = f"De geraamde kans op een tekort is {probability * 100:.1f}%; aanvullende monitoring blijft gewenst."
        confidence = "MIDDEL"
    else:
        risk_text = f"De geraamde kans op een tekort is nog {probability * 100:.1f}%; het advies is daarom voorwaardelijk."
        confidence = "LAAG"

    timing = "zonder verschuiving" if shift == 0 else (f"{abs(shift)} jaar later" if shift > 0 else f"{abs(shift)} jaar eerder")
    recommendation = Recommendation(
        title=f"Voorkeursstrategie: {scenario}",
        decision=(
            f"Kies scenario {scenario}, plan de onderhoudsstrategie {timing}, "
            f"hanteer een jaarlijkse VvE-bijdrage van {_money(contribution)} en een extra reservebuffer van {_money(buffer)}."
        ),
        rationale=(
            "Deze combinatie heeft binnen de doorgerekende opties de beste balans tussen totale financieringslast, "
            "onderhoudstiming, tekortrisico en duurzaamheid."
        ),
        financial_effect=(
            f"Indicatief komt de bijdrage uit op €{monthly:,.2f} per appartement per maand; "
            f"de totale MJOP-last binnen de strategie bedraagt circa {_money(total_mjop)}."
        ).replace(",", "X").replace(".", ",").replace("X", "."),
        risk_effect=risk_text,
        sustainability_effect=f"De strategie behaalt een duurzaamheidsscore van {sustainability:.1f}/100.",
        rejected_alternatives=rejected,
        confidence=confidence,
    )

    return {
        "status": "ADVIES GEREED",
        "recommendation": asdict(recommendation),
        "decision_summary": recommendation.decision,
        "key_metrics": {
            "scenario": scenario,
            "monthly_per_apartment": round(monthly, 2),
            "reserve_buffer": round(buffer, 2),
            "deficit_probability": round(probability, 4),
            "sustainability_score": round(sustainability, 2),
        },
    }
