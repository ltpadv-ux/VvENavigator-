"""Core domain calculations for the VvE Navigator MVP."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class MaintenanceItem:
    """A planned maintenance intervention."""

    component: str
    year: int
    base_cost: float
    risk_score: float = 0.0

    def indexed_cost(self, inflation_rate: float, base_year: int) -> float:
        years = max(0, self.year - base_year)
        return self.base_cost * ((1 + inflation_rate) ** years)


def net_present_value(cashflows: Iterable[float], discount_rate: float) -> float:
    """Return NPV for cashflows where the first value is year 0."""
    if discount_rate <= -1:
        raise ValueError("discount_rate must be greater than -1")
    return sum(value / ((1 + discount_rate) ** year) for year, value in enumerate(cashflows))


def maintenance_priority(risk_score: float, urgency: float, budget_impact: float) -> float:
    """Combine normalized risk drivers into a 0-100 decision priority."""
    values = (risk_score, urgency, budget_impact)
    if any(value < 0 or value > 100 for value in values):
        raise ValueError("risk_score, urgency and budget_impact must be 0-100")
    return round(0.5 * risk_score + 0.3 * urgency + 0.2 * budget_impact, 2)
