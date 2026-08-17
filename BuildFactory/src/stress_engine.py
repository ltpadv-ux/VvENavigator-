"""Stress test and Monte Carlo engine for VvE Navigator."""
from __future__ import annotations

from dataclasses import dataclass, asdict
import random
from statistics import mean
from typing import Iterable


@dataclass(frozen=True)
class StressAssumptions:
    inflation_mean: float = 0.04
    inflation_std: float = 0.015
    cost_overrun_mean: float = 0.08
    cost_overrun_std: float = 0.06
    delay_probability: float = 0.15
    unexpected_cost_probability: float = 0.10
    unexpected_cost_fraction: float = 0.10


def _percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    index = (len(values) - 1) * p
    lower = int(index)
    upper = min(lower + 1, len(values) - 1)
    weight = index - lower
    return values[lower] * (1 - weight) + values[upper] * weight


def run_monte_carlo(
    start_year: int,
    years: int,
    opening_reserve: float,
    annual_contribution: float,
    annual_operating_costs: float,
    mjop_costs: dict[int, float],
    simulations: int = 1000,
    assumptions: StressAssumptions | None = None,
    seed: int | None = 42,
) -> dict:
    """Simulate reserve outcomes under cost, inflation and timing uncertainty."""
    if years <= 0 or simulations <= 0:
        raise ValueError("years and simulations must be positive")
    if opening_reserve < 0:
        raise ValueError("opening_reserve must be non-negative")
    assumptions = assumptions or StressAssumptions()
    rng = random.Random(seed)

    ending_reserves: list[float] = []
    minimum_reserves: list[float] = []
    deficit_runs = 0
    yearly_deficit_counts = {start_year + offset: 0 for offset in range(years)}

    for _ in range(simulations):
        reserve = float(opening_reserve)
        minimum = reserve
        delayed: dict[int, float] = {}
        ever_deficit = False

        for offset in range(years):
            year = start_year + offset
            inflation = max(-0.02, rng.gauss(assumptions.inflation_mean, assumptions.inflation_std))
            contribution = annual_contribution * ((1 + inflation) ** offset)
            operating = annual_operating_costs * ((1 + inflation) ** offset)

            base_mjop = float(mjop_costs.get(year, 0.0)) + delayed.pop(year, 0.0)
            if base_mjop > 0 and rng.random() < assumptions.delay_probability and offset < years - 1:
                delayed[year + 1] = delayed.get(year + 1, 0.0) + base_mjop
                base_mjop = 0.0

            overrun = max(-0.25, rng.gauss(assumptions.cost_overrun_mean, assumptions.cost_overrun_std))
            stressed_mjop = base_mjop * max(0.0, 1 + overrun)

            unexpected = 0.0
            if rng.random() < assumptions.unexpected_cost_probability:
                unexpected = max(opening_reserve, annual_operating_costs) * assumptions.unexpected_cost_fraction

            reserve += contribution - operating - stressed_mjop - unexpected
            minimum = min(minimum, reserve)
            if reserve < 0:
                yearly_deficit_counts[year] += 1
                ever_deficit = True

        ending_reserves.append(reserve)
        minimum_reserves.append(minimum)
        if ever_deficit:
            deficit_runs += 1

    probability_deficit = deficit_runs / simulations
    yearly_probability = {year: round(count / simulations, 4) for year, count in yearly_deficit_counts.items()}

    return {
        "simulations": simulations,
        "probability_of_deficit": round(probability_deficit, 4),
        "ending_reserve_mean": round(mean(ending_reserves), 2),
        "ending_reserve_p10": round(_percentile(ending_reserves, 0.10), 2),
        "ending_reserve_p50": round(_percentile(ending_reserves, 0.50), 2),
        "ending_reserve_p90": round(_percentile(ending_reserves, 0.90), 2),
        "minimum_reserve_mean": round(mean(minimum_reserves), 2),
        "yearly_deficit_probability": yearly_probability,
        "risk_level": stress_risk_level(probability_deficit),
        "assumptions": asdict(assumptions),
    }


def stress_risk_level(probability_of_deficit: float) -> str:
    if probability_of_deficit >= 0.50:
        return "KRITIEK"
    if probability_of_deficit >= 0.25:
        return "HOOG"
    if probability_of_deficit >= 0.10:
        return "AANDACHT"
    return "BEHEERSBAAR"


def stress_summary(results: Iterable[dict]) -> dict:
    rows = list(results)
    if not rows:
        return {"runs": 0, "critical": 0, "high": 0, "average_deficit_probability": 0.0}
    probabilities = [float(row.get("probability_of_deficit", 0.0)) for row in rows]
    return {
        "runs": len(rows),
        "critical": sum(1 for row in rows if row.get("risk_level") == "KRITIEK"),
        "high": sum(1 for row in rows if row.get("risk_level") == "HOOG"),
        "average_deficit_probability": round(mean(probabilities), 4),
    }
