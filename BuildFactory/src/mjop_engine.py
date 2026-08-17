"""MJOP planning engine for the VvE Navigator.

The engine deliberately keeps cost assumptions explicit so they can later be
replaced by the central Dutch cost-kengetallen library.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class MJOPComponent:
    """One maintainable building component in an MJOP."""

    component: str
    bouwdeel: str
    quantity: float
    unit: str
    unit_cost: float
    interval_years: int
    last_execution_year: int
    condition_score: int = 3
    risk_score: float = 0.0
    urgency: float = 0.0
    budget_impact: float = 0.0

    def __post_init__(self) -> None:
        if self.quantity < 0 or self.unit_cost < 0:
            raise ValueError("quantity and unit_cost must be non-negative")
        if self.interval_years <= 0:
            raise ValueError("interval_years must be greater than zero")
        if not 1 <= self.condition_score <= 6:
            raise ValueError("condition_score must be between 1 and 6")

    @property
    def base_cost(self) -> float:
        return self.quantity * self.unit_cost

    def next_execution_year(self) -> int:
        return self.last_execution_year + self.interval_years

    def priority(self) -> float:
        from vve_navigator import maintenance_priority

        return maintenance_priority(self.risk_score, self.urgency, self.budget_impact)


def generate_plan(
    components: Iterable[MJOPComponent],
    start_year: int,
    horizon_years: int = 30,
    inflation_rate: float = 0.04,
) -> list[dict]:
    """Generate annual MJOP interventions with indexed costs.

    The returned records are intentionally flat, making them easy to export to
    Excel, Power BI or a relational DataHub later.
    """
    if horizon_years < 1:
        raise ValueError("horizon_years must be at least 1")
    if inflation_rate <= -1:
        raise ValueError("inflation_rate must be greater than -1")

    end_year = start_year + horizon_years - 1
    plan: list[dict] = []
    for item in components:
        year = item.next_execution_year()
        while year <= end_year:
            years_from_start = year - start_year
            indexed_cost = item.base_cost * ((1 + inflation_rate) ** years_from_start)
            plan.append(
                {
                    "year": year,
                    "component": item.component,
                    "bouwdeel": item.bouwdeel,
                    "quantity": item.quantity,
                    "unit": item.unit,
                    "base_cost": round(item.base_cost, 2),
                    "indexed_cost": round(indexed_cost, 2),
                    "condition_score": item.condition_score,
                    "priority": item.priority(),
                }
            )
            year += item.interval_years

    return sorted(plan, key=lambda row: (row["year"], -row["priority"], row["bouwdeel"]))


def annual_totals(plan: Iterable[dict]) -> dict[int, float]:
    """Aggregate indexed MJOP costs by execution year."""
    totals: dict[int, float] = {}
    for row in plan:
        year = int(row["year"])
        totals[year] = round(totals.get(year, 0.0) + float(row["indexed_cost"]), 2)
    return dict(sorted(totals.items()))


def reserve_gap(reserve_fund: float, plan: Iterable[dict], year: int) -> float:
    """Return reserve after the selected year's planned interventions."""
    if reserve_fund < 0:
        raise ValueError("reserve_fund must be non-negative")
    spend = sum(float(row["indexed_cost"]) for row in plan if int(row["year"]) == year)
    return round(reserve_fund - spend, 2)
