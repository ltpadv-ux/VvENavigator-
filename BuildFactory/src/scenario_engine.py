"""Scenario engine for comparing VvE maintenance and sustainability strategies."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Scenario:
    name: str
    cost_factor: float = 1.0
    energy_saving: float = 0.0
    co2_reduction: float = 0.0
    start_shift_years: int = 0


def compare_scenarios(
    base_annual_costs: dict[int, float],
    scenarios: Iterable[Scenario],
    reserve_fund: float = 0.0,
) -> list[dict]:
    """Return comparable 30-year financial and sustainability indicators."""
    results: list[dict] = []
    base_total = sum(base_annual_costs.values())
    for scenario in scenarios:
        shifted_total = 0.0
        annual: dict[int, float] = {}
        for year, amount in base_annual_costs.items():
            target_year = int(year) + scenario.start_shift_years
            value = float(amount) * scenario.cost_factor
            annual[target_year] = round(annual.get(target_year, 0.0) + value, 2)
            shifted_total += value
        first_year = min(annual) if annual else None
        first_year_spend = annual.get(first_year, 0.0) if first_year else 0.0
        results.append({
            "scenario": scenario.name,
            "total_mjop": round(shifted_total, 2),
            "delta_vs_base": round(shifted_total - base_total, 2),
            "reserve_after_first_intervention": round(reserve_fund - first_year_spend, 2),
            "energy_saving_pct": round(scenario.energy_saving * 100, 1),
            "co2_reduction_pct": round(scenario.co2_reduction * 100, 1),
            "annual_costs": dict(sorted(annual.items())),
        })
    return results
