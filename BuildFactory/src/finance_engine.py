"""Financial planning engine for the VvE Navigator."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class FinanceYear:
    year: int
    contribution_income: float = 0.0
    other_income: float = 0.0
    operating_expenses: float = 0.0
    mjop_expenses: float = 0.0
    reserve_opening: float = 0.0

    @property
    def total_income(self) -> float:
        return self.contribution_income + self.other_income

    @property
    def total_expenses(self) -> float:
        return self.operating_expenses + self.mjop_expenses

    @property
    def result(self) -> float:
        return self.total_income - self.total_expenses

    @property
    def reserve_closing(self) -> float:
        return self.reserve_opening + self.result


def build_cashflow(
    years: Iterable[FinanceYear],
    inflation_rate: float = 0.0,
    base_year: int | None = None,
) -> list[dict]:
    """Build a sequential cashflow and reserve-fund projection."""
    if inflation_rate < -1:
        raise ValueError("inflation_rate must be greater than -1")
    rows: list[dict] = []
    reserve = 0.0
    for item in sorted(years, key=lambda x: x.year):
        opening = reserve if rows else item.reserve_opening
        year_index = max(0, item.year - (base_year or item.year))
        factor = (1 + inflation_rate) ** year_index
        income = item.total_income * factor
        expenses = item.total_expenses * factor
        result = income - expenses
        reserve = opening + result
        rows.append({
            "year": item.year,
            "income": round(income, 2),
            "expenses": round(expenses, 2),
            "result": round(result, 2),
            "reserve_opening": round(opening, 2),
            "reserve_closing": round(reserve, 2),
        })
    return rows


def liquidity_gap(cash_available: float, required_reserve: float) -> float:
    """Return the amount missing to meet the required reserve."""
    if cash_available < 0 or required_reserve < 0:
        raise ValueError("cash_available and required_reserve must be non-negative")
    return round(max(0.0, required_reserve - cash_available), 2)


def annual_contribution_needed(
    reserve_gap: float,
    apartments: int,
    years: int = 1,
) -> float:
    """Calculate additional contribution per apartment needed to close a gap."""
    if reserve_gap < 0 or apartments <= 0 or years <= 0:
        raise ValueError("reserve_gap >= 0, apartments > 0 and years > 0 are required")
    return round(reserve_gap / apartments / years, 2)
