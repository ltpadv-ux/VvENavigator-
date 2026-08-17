"""Decision Intelligence Platform orchestration for VvE Navigator Enterprise 3.0."""
from __future__ import annotations

from typing import Any

from recommendation_engine import explain_strategy


DECISION_INTELLIGENCE_VERSION = "3.0.0"


def build_decision_intelligence(
    forecast: dict[str, Any],
    stress: dict[str, Any],
    optimization: dict[str, Any],
    strategy: dict[str, Any],
    apartments: int,
) -> dict[str, Any]:
    """Combine predictive, probabilistic and optimization outputs into one board decision layer."""
    recommendation = explain_strategy(strategy, apartments)

    forecast_status = str(forecast.get("status", "ONBEKEND"))
    stress_level = str(stress.get("risk_level", "ONBEKEND"))
    optimization_status = str(optimization.get("status", "ONBEKEND"))
    advice_status = str(recommendation.get("status", "GEEN ADVIES"))

    blocking_reasons: list[str] = []
    if forecast_status == "ACTIE NODIG":
        blocking_reasons.append("Forecast signaleert toekomstige druk")
    if stress_level in {"HOOG", "KRITIEK"}:
        blocking_reasons.append(f"Stress-test risico is {stress_level.lower()}")
    if optimization_status in {"GEEN OPLOSSING", "GEEN ROBUUSTE OPLOSSING"}:
        blocking_reasons.append("Geen robuuste financiële optimalisatie gevonden")
    if advice_status != "ADVIES GEREED":
        blocking_reasons.append("Bestuursadvies is nog niet gereed")

    readiness_score = 100.0
    readiness_score -= 20.0 if forecast_status == "ACTIE NODIG" else 0.0
    readiness_score -= 30.0 if stress_level == "KRITIEK" else (15.0 if stress_level == "HOOG" else 0.0)
    readiness_score -= 25.0 if optimization_status in {"GEEN OPLOSSING", "GEEN ROBUUSTE OPLOSSING"} else 0.0
    readiness_score -= 25.0 if advice_status != "ADVIES GEREED" else 0.0
    readiness_score = round(max(0.0, readiness_score), 2)

    if readiness_score >= 80 and not blocking_reasons:
        status = "BESLUITRIJP"
    elif readiness_score >= 50:
        status = "VOORBEREIDEN"
    else:
        status = "HERZIEN"

    return {
        "platform_version": DECISION_INTELLIGENCE_VERSION,
        "status": status,
        "readiness_score": readiness_score,
        "blocking_reasons": blocking_reasons,
        "forecast": forecast,
        "stress_test": stress,
        "optimization": optimization,
        "strategy": strategy,
        "recommendation": recommendation,
        "board_decision": recommendation.get("decision_summary", "Nog geen besluitadvies beschikbaar"),
        "key_metrics": {
            **recommendation.get("key_metrics", {}),
            "forecast_status": forecast_status,
            "stress_level": stress_level,
            "optimization_status": optimization_status,
        },
    }
