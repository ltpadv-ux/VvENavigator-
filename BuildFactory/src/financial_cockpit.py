"""Financial Cockpit for long-term VvE reserve and contribution planning."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class FinancialAssumptions:
    annual_contribution_total: float
    annual_operating_costs: float
    contribution_growth: float = 0.02
    operating_cost_growth: float = 0.02
    reserve_interest: float = 0.01


def project_reserve(
    start_year: int,
    years: int,
    opening_reserve: float,
    mjop_costs: dict[int, float],
    assumptions: FinancialAssumptions,
) -> list[dict]:
    if years <= 0:
        raise ValueError("years must be positive")
    if opening_reserve < 0:
        raise ValueError("opening_reserve must be non-negative")
    reserve = float(opening_reserve)
    rows: list[dict] = []
    for offset in range(years):
        year = start_year + offset
        contribution = assumptions.annual_contribution_total * ((1 + assumptions.contribution_growth) ** offset)
        operating = assumptions.annual_operating_costs * ((1 + assumptions.operating_cost_growth) ** offset)
        interest = max(0.0, reserve) * assumptions.reserve_interest
        mjop = float(mjop_costs.get(year, 0.0))
        opening = reserve
        reserve = opening + contribution + interest - operating - mjop
        rows.append({
            "year": year,
            "reserve_opening": round(opening, 2),
            "contribution": round(contribution, 2),
            "interest": round(interest, 2),
            "operating_costs": round(operating, 2),
            "mjop_costs": round(mjop, 2),
            "reserve_closing": round(reserve, 2),
            "liquidity_status": "TEKORT" if reserve < 0 else "OK",
        })
    return rows


def minimum_reserve(projection: Iterable[dict]) -> tuple[int | None, float]:
    rows = list(projection)
    if not rows:
        return None, 0.0
    lowest = min(rows, key=lambda row: float(row["reserve_closing"]))
    return int(lowest["year"]), float(lowest["reserve_closing"])


def required_contribution_for_nonnegative_reserve(
    start_year: int,
    years: int,
    opening_reserve: float,
    mjop_costs: dict[int, float],
    annual_operating_costs: float,
    apartments: int,
    growth: float = 0.02,
) -> dict:
    """Binary-search the annual contribution needed to keep reserves non-negative."""
    if apartments <= 0:
        raise ValueError("apartments must be positive")
    low, high = 0.0, max(sum(mjop_costs.values()) / max(years, 1) + annual_operating_costs, 1.0) * 3
    for _ in range(60):
        mid = (low + high) / 2
        projection = project_reserve(
            start_year, years, opening_reserve, mjop_costs,
            FinancialAssumptions(mid, annual_operating_costs, growth, growth, 0.0),
        )
        _, minimum = minimum_reserve(projection)
        if minimum < 0:
            low = mid
        else:
            high = mid
    annual_total = round(high, 2)
    return {
        "annual_contribution_total": annual_total,
        "annual_per_apartment": round(annual_total / apartments, 2),
        "monthly_per_apartment": round(annual_total / apartments / 12, 2),
    }


def cockpit_summary(projection: Iterable[dict], apartments: int) -> dict:
    rows = list(projection)
    year, minimum = minimum_reserve(rows)
    deficits = [row for row in rows if row["reserve_closing"] < 0]
    return {
        "horizon_years": len(rows),
        "minimum_reserve_year": year,
        "minimum_reserve": round(minimum, 2),
        "first_deficit_year": deficits[0]["year"] if deficits else None,
        "ending_reserve": rows[-1]["reserve_closing"] if rows else 0.0,
        "apartments": apartments,
        "status": "ACTIE NODIG" if deficits else "VOLDOENDE",
    }
