"""Portfolio analytics for multiple VvE Navigator enterprise releases."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Iterable


@dataclass(frozen=True)
class PortfolioItem:
    name: str
    status: str
    health_status: str
    health_score: float
    vni: float
    reserve_fund: float
    risk_score: float
    mjop_pressure: float
    investment_need: float
    publishable: bool


def portfolio_item(name: str, enterprise_result: dict[str, Any]) -> PortfolioItem:
    release = enterprise_result.get("release", {})
    dashboard = release.get("dashboard", {})
    quality = release.get("quality_gate", {})
    health = enterprise_result.get("health", {})
    totals = release.get("annual_mjop_totals", {})

    reserve = float(dashboard.get("reserve_fund", dashboard.get("reserve", 0.0)) or 0.0)
    risk = float(dashboard.get("risk_score", 0.0) or 0.0)
    vni = float(dashboard.get("vni", dashboard.get("VNI", 0.0)) or 0.0)
    annual_peak = max((float(v) for v in totals.values()), default=0.0)
    mjop_pressure = round(min(100.0, annual_peak / max(reserve, 1.0) * 100.0), 2)
    investment_need = round(max(0.0, annual_peak - reserve), 2)

    return PortfolioItem(
        name=name,
        status=str(enterprise_result.get("status", "UNKNOWN")),
        health_status=str(health.get("status", "UNKNOWN")),
        health_score=float(health.get("health_score", 0.0) or 0.0),
        vni=round(vni, 2),
        reserve_fund=round(reserve, 2),
        risk_score=round(risk, 2),
        mjop_pressure=mjop_pressure,
        investment_need=investment_need,
        publishable=bool(quality.get("can_publish", release.get("publishable", False))),
    )


def portfolio_summary(items: Iterable[PortfolioItem]) -> dict[str, Any]:
    rows = list(items)
    count = len(rows)
    total_reserve = sum(item.reserve_fund for item in rows)
    total_need = sum(item.investment_need for item in rows)
    avg_vni = sum(item.vni for item in rows) / count if count else 0.0
    avg_health = sum(item.health_score for item in rows) / count if count else 0.0
    avg_risk = sum(item.risk_score for item in rows) / count if count else 0.0

    ranked = sorted(rows, key=lambda x: (-x.investment_need, -x.risk_score, x.name))
    return {
        "portfolio_count": count,
        "total_reserve_fund": round(total_reserve, 2),
        "total_investment_need": round(total_need, 2),
        "average_vni": round(avg_vni, 2),
        "average_health_score": round(avg_health, 2),
        "average_risk_score": round(avg_risk, 2),
        "ready_count": sum(1 for item in rows if item.status == "READY"),
        "blocked_count": sum(1 for item in rows if item.status == "BLOCKED"),
        "error_count": sum(1 for item in rows if item.status == "ERROR"),
        "healthy_count": sum(1 for item in rows if item.health_status == "HEALTHY"),
        "degraded_count": sum(1 for item in rows if item.health_status == "DEGRADED"),
        "critical_count": sum(1 for item in rows if item.health_status == "CRITICAL"),
        "publishable_count": sum(1 for item in rows if item.publishable),
        "priority_vves": [asdict(item) for item in ranked[:5]],
        "items": [asdict(item) for item in rows],
    }


def build_portfolio(results: Iterable[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
    """Convert named Enterprise results into one portfolio dashboard payload."""
    return portfolio_summary(portfolio_item(name, result) for name, result in results)
