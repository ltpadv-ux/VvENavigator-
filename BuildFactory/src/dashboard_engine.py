"""Decision dashboard calculations for the VvE Navigator."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class DashboardInput:
    reserve_fund: float
    required_reserve: float
    annual_mjop: float
    annual_budget: float
    risk_score: float
    condition_score: float = 3.0
    liquidity: float | None = None


def _bounded(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 2)


def reserve_score(reserve_fund: float, required_reserve: float) -> float:
    if reserve_fund < 0 or required_reserve < 0:
        raise ValueError("reserve values must be non-negative")
    if required_reserve == 0:
        return 100.0
    return _bounded(100 * reserve_fund / required_reserve)


def mjop_score(annual_mjop: float, annual_budget: float) -> float:
    if annual_mjop < 0 or annual_budget < 0:
        raise ValueError("MJOP and budget must be non-negative")
    if annual_budget == 0:
        return 100.0 if annual_mjop == 0 else 0.0
    return _bounded(100 * (1 - annual_mjop / annual_budget))


def condition_score(condition: float) -> float:
    if not 1 <= condition <= 6:
        raise ValueError("condition_score must be between 1 and 6")
    return _bounded((6 - condition) / 5 * 100)


def vni_score(data: DashboardInput) -> float:
    """VvE Navigator Index: financial + MJOP + risk + condition health."""
    return round(
        0.35 * reserve_score(data.reserve_fund, data.required_reserve)
        + 0.25 * mjop_score(data.annual_mjop, data.annual_budget)
        + 0.25 * _bounded(100 - data.risk_score)
        + 0.15 * condition_score(data.condition_score),
        2,
    )


def mgi_score(annual_mjop: float, annual_budget: float) -> float:
    """Maintenance Governance Index: remaining budget headroom."""
    return mjop_score(annual_mjop, annual_budget)


def status(score: float) -> str:
    if not 0 <= score <= 100:
        raise ValueError("score must be between 0 and 100")
    if score >= 75:
        return "GROEN"
    if score >= 50:
        return "GEEL"
    if score >= 25:
        return "ORANJE"
    return "ROOD"


def top_actions(risks: Iterable[dict], limit: int = 3) -> list[dict]:
    """Return highest-priority actions for the board dashboard."""
    if limit <= 0:
        raise ValueError("limit must be positive")
    rows = sorted(risks, key=lambda row: row.get("priority", row.get("risk_score", 0)), reverse=True)
    return rows[:limit]


def build_dashboard(data: DashboardInput, risks: Iterable[dict] = ()) -> dict:
    vni = vni_score(data)
    mgi = mgi_score(data.annual_mjop, data.annual_budget)
    reserve = reserve_score(data.reserve_fund, data.required_reserve)
    return {
        "vni": vni,
        "vni_status": status(vni),
        "mgi": mgi,
        "mgi_status": status(mgi),
        "reserve_score": reserve,
        "reserve_status": status(reserve),
        "risk_score": round(data.risk_score, 2),
        "risk_status": status(100 - data.risk_score),
        "condition_score": round(data.condition_score, 2),
        "top_3_actions": top_actions(risks, 3),
    }
