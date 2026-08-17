"""Forecast and predictive early-warning engine for VvE Navigator."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable


@dataclass(frozen=True)
class ForecastSignal:
    year: int
    reserve: float
    mjop_costs: float
    risk_score: float
    pressure_score: float
    level: str
    message: str


def pressure_score(reserve: float, mjop_costs: float, risk_score: float, reserve_floor: float = 0.0) -> float:
    """Return a 0-100 forward pressure score from reserve, MJOP and risk."""
    reserve_gap = max(0.0, reserve_floor - reserve)
    reserve_risk = min(100.0, reserve_gap / max(abs(reserve_floor), 1.0) * 100.0) if reserve_floor > 0 else (100.0 if reserve < 0 else 0.0)
    spend_risk = min(100.0, mjop_costs / max(max(reserve, 0.0), 1.0) * 100.0)
    return round(0.45 * reserve_risk + 0.35 * spend_risk + 0.20 * max(0.0, min(100.0, risk_score)), 2)


def warning_level(score: float) -> str:
    if score >= 75:
        return "KRITIEK"
    if score >= 50:
        return "WAARSCHUWING"
    if score >= 25:
        return "AANDACHT"
    return "STABIEL"


def forecast_signals(
    reserve_projection: Iterable[dict],
    annual_mjop: dict[int, float],
    risk_by_year: dict[int, float] | None = None,
    reserve_floor: float = 0.0,
) -> list[dict]:
    """Generate year-by-year predictive early-warning signals."""
    risk_by_year = risk_by_year or {}
    signals: list[ForecastSignal] = []
    for row in reserve_projection:
        year = int(row["year"])
        reserve = float(row.get("reserve_closing", 0.0))
        mjop = float(annual_mjop.get(year, row.get("mjop_costs", 0.0)))
        risk = float(risk_by_year.get(year, 0.0))
        score = pressure_score(reserve, mjop, risk, reserve_floor)
        level = warning_level(score)
        if reserve < 0:
            message = "Reserve wordt negatief; financieringsmaatregel voorbereiden"
        elif reserve_floor and reserve < reserve_floor:
            message = "Reserve daalt onder beleidsvloer"
        elif mjop > max(reserve, 1.0) * 0.5:
            message = "Hoge onderhoudspiek ten opzichte van reserve"
        elif risk >= 50:
            message = "Technisch risico vraagt versnelde voorbereiding"
        else:
            message = "Geen vroegtijdig knelpunt voorzien"
        signals.append(ForecastSignal(year, reserve, mjop, risk, score, level, message))
    return [asdict(item) for item in signals]


def forecast_summary(signals: Iterable[dict], lookahead_years: int = 5) -> dict:
    rows = list(signals)
    future = rows[:lookahead_years] if lookahead_years > 0 else rows
    alerts = [row for row in future if row["level"] in {"KRITIEK", "WAARSCHUWING"}]
    highest = max(future, key=lambda row: float(row["pressure_score"]), default=None)
    first_critical = next((row["year"] for row in future if row["level"] == "KRITIEK"), None)
    return {
        "lookahead_years": min(lookahead_years, len(rows)) if lookahead_years > 0 else len(rows),
        "alert_count": len(alerts),
        "first_critical_year": first_critical,
        "highest_pressure_year": highest["year"] if highest else None,
        "highest_pressure_score": highest["pressure_score"] if highest else 0.0,
        "status": "ACTIE NODIG" if alerts else "STABIEL",
    }
