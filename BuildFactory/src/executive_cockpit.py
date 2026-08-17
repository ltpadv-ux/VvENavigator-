"""Executive cockpit for VvE Navigator Decision Intelligence Platform."""
from __future__ import annotations

from typing import Any, Iterable


def _top_actions(actions: Iterable[str], limit: int = 3) -> list[str]:
    result: list[str] = []
    for action in actions:
        text = str(action).strip()
        if text and text not in result:
            result.append(text)
        if len(result) >= limit:
            break
    return result


def build_executive_cockpit(
    decision_intelligence: dict[str, Any],
    dashboard: dict[str, Any] | None = None,
    financial: dict[str, Any] | None = None,
    health: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create one compact board view from the main decision layers."""
    dashboard = dashboard or {}
    financial = financial or {}
    health = health or {}

    metrics = dict(decision_intelligence.get("key_metrics") or {})
    readiness = float(decision_intelligence.get("readiness_score", 0.0))
    status = str(decision_intelligence.get("status", "VOORBEREIDEN"))
    board_decision = str(decision_intelligence.get("board_decision", "Nog geen eindadvies beschikbaar"))

    vni = float(dashboard.get("vni", dashboard.get("VNI", 0.0)) or 0.0)
    reserve = float(financial.get("ending_reserve", financial.get("reserve_fund", dashboard.get("reserve_fund", 0.0))) or 0.0)
    deficit_probability = float(metrics.get("deficit_probability", 0.0) or 0.0)
    monthly = float(metrics.get("monthly_per_apartment", 0.0) or 0.0)
    strategy = str(metrics.get("scenario", decision_intelligence.get("best_strategy", {}).get("scenario", "Onbekend")))
    health_score = float(health.get("health_score", 0.0) or 0.0)

    action_candidates = []
    action_candidates.extend(decision_intelligence.get("blocking_reasons", []) or [])
    recommendation = decision_intelligence.get("recommendation") or {}
    rec_obj = recommendation.get("recommendation") if isinstance(recommendation, dict) else {}
    if isinstance(rec_obj, dict):
        action_candidates.extend(rec_obj.get("rejected_alternatives", []) or [])
    if board_decision:
        action_candidates.insert(0, board_decision)

    top_actions = _top_actions(action_candidates, 3)
    while len(top_actions) < 3:
        fallbacks = [
            "Actualiseer MJOP en reserveprognose",
            "Leg voorkeursstrategie ter besluitvorming voor",
            "Monitor risico en liquiditeit per kwartaal",
        ]
        for fallback in fallbacks:
            if fallback not in top_actions:
                top_actions.append(fallback)
            if len(top_actions) >= 3:
                break

    return {
        "cockpit": "Executive Cockpit",
        "status": status,
        "decision_readiness": round(readiness, 2),
        "vni": round(vni, 2),
        "reserve": round(reserve, 2),
        "deficit_probability": round(deficit_probability, 4),
        "best_strategy": strategy,
        "monthly_per_apartment": round(monthly, 2),
        "health_score": round(health_score, 2),
        "board_decision": board_decision,
        "top_actions": top_actions,
    }
