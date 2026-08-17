"""Decision engine for VvE Navigator board recommendations."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable


@dataclass(frozen=True)
class Decision:
    action: str
    priority: str
    score: float
    rationale: str
    horizon: str


def decision_score(risk_score: float, condition_score: int, liquidity_gap: float, annual_mjop: float) -> float:
    """Combine risk, technical condition and liquidity stress into 0-100."""
    if not 1 <= condition_score <= 6:
        raise ValueError("condition_score must be between 1 and 6")
    if liquidity_gap < 0 or annual_mjop < 0:
        raise ValueError("liquidity_gap and annual_mjop must be non-negative")
    condition_risk = (condition_score - 1) / 5 * 100
    liquidity_risk = min(100.0, liquidity_gap / max(annual_mjop, 1.0) * 100)
    return round(0.5 * risk_score + 0.3 * condition_risk + 0.2 * liquidity_risk, 2)


def priority_label(score: float) -> str:
    if score >= 75:
        return "NU"
    if score >= 50:
        return "HOOG"
    if score >= 25:
        return "PLANNEN"
    return "MONITOREN"


def advise_component(
    component: str,
    risk_score: float,
    condition_score: int,
    liquidity_gap: float,
    annual_mjop: float,
    sustainability_gain: float = 0.0,
) -> Decision:
    score = decision_score(risk_score, condition_score, liquidity_gap, annual_mjop)
    priority = priority_label(score)
    if priority == "NU":
        action = f"{component}: nu uitvoeren of technisch veiligstellen"
        horizon = "0-1 jaar"
    elif priority == "HOOG":
        action = f"{component}: opnemen in eerstvolgende begroting"
        horizon = "1-2 jaar"
    elif priority == "PLANNEN":
        action = f"{component}: planmatig reserveren en voorbereiden"
        horizon = "2-5 jaar"
    else:
        action = f"{component}: monitoren binnen regulier MJOP"
        horizon = "5+ jaar"

    if sustainability_gain >= 10:
        action += "; combineer waar mogelijk met verduurzaming"

    rationale = (
        f"Risico {risk_score:.0f}/100, conditie {condition_score}/6, "
        f"liquiditeitsdruk €{liquidity_gap:,.0f}."
    )
    return Decision(action, priority, score, rationale, horizon)


def board_decisions(items: Iterable[dict], top_n: int = 5) -> list[dict]:
    """Rank board decisions from component-level inputs."""
    decisions = [
        advise_component(
            str(item["component"]),
            float(item.get("risk_score", 0.0)),
            int(item.get("condition_score", 3)),
            float(item.get("liquidity_gap", 0.0)),
            float(item.get("annual_mjop", 0.0)),
            float(item.get("sustainability_gain", 0.0)),
        )
        for item in items
    ]
    decisions.sort(key=lambda d: (-d.score, d.action))
    return [asdict(item) for item in decisions[:top_n]]
