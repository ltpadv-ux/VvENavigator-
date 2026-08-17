"""Strategy optimizer for 30-year VvE maintenance and sustainability planning."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable

from scenario_engine import Scenario, compare_scenarios
from stress_engine import run_monte_carlo, StressAssumptions


@dataclass(frozen=True)
class StrategyCandidate:
    scenario: str
    shift_years: int
    annual_contribution: float
    reserve_buffer: float
    deficit_probability: float
    total_mjop: float
    sustainability_score: float
    objective_score: float


def _sustainability_score(energy_saving_pct: float, co2_reduction_pct: float) -> float:
    return round(0.5 * max(0.0, min(100.0, energy_saving_pct)) + 0.5 * max(0.0, min(100.0, co2_reduction_pct)), 2)


def optimize_strategy(
    start_year: int,
    years: int,
    opening_reserve: float,
    base_annual_costs: dict[int, float],
    scenarios: Iterable[Scenario],
    annual_operating_costs: float,
    contribution_options: Iterable[float],
    reserve_buffer_options: Iterable[float],
    shift_options: Iterable[int] = (-1, 0, 1, 2),
    target_deficit_probability: float = 0.05,
    simulations: int = 400,
    seed: int = 42,
    stress_assumptions: StressAssumptions | None = None,
) -> dict:
    """Find the lowest-cost robust 30-year strategy across scenario, timing and funding."""
    if years <= 0:
        raise ValueError("years must be positive")
    if not 0 <= target_deficit_probability <= 1:
        raise ValueError("target_deficit_probability must be between 0 and 1")

    candidates: list[StrategyCandidate] = []
    scenario_list = list(scenarios)
    for scenario in scenario_list:
        for shift in shift_options:
            shifted = Scenario(
                name=scenario.name,
                cost_factor=scenario.cost_factor,
                energy_saving=scenario.energy_saving,
                co2_reduction=scenario.co2_reduction,
                start_shift_years=scenario.start_shift_years + int(shift),
            )
            result = compare_scenarios(base_annual_costs, [shifted], opening_reserve)[0]
            annual_costs = {int(y): float(v) for y, v in result["annual_costs"].items()}
            sustainability = _sustainability_score(result["energy_saving_pct"], result["co2_reduction_pct"])

            for contribution in contribution_options:
                for buffer in reserve_buffer_options:
                    stress = run_monte_carlo(
                        start_year=start_year,
                        years=years,
                        opening_reserve=opening_reserve + float(buffer),
                        annual_contribution=float(contribution),
                        annual_operating_costs=float(annual_operating_costs),
                        mjop_costs=annual_costs,
                        simulations=simulations,
                        assumptions=stress_assumptions,
                        seed=seed,
                    )
                    probability = float(stress["probability_of_deficit"])
                    financing_cost = float(contribution) * years + float(buffer)
                    timing_penalty = abs(int(shift)) * max(sum(base_annual_costs.values()) * 0.002, 1.0)
                    sustainability_credit = sustainability * max(sum(base_annual_costs.values()) * 0.0005, 1.0)
                    risk_penalty = probability * max(financing_cost, 1.0)
                    objective = financing_cost + timing_penalty + risk_penalty - sustainability_credit
                    candidates.append(StrategyCandidate(
                        scenario=scenario.name,
                        shift_years=int(shifted.start_shift_years),
                        annual_contribution=round(float(contribution), 2),
                        reserve_buffer=round(float(buffer), 2),
                        deficit_probability=round(probability, 4),
                        total_mjop=round(float(result["total_mjop"]), 2),
                        sustainability_score=sustainability,
                        objective_score=round(objective, 2),
                    ))

    feasible = [c for c in candidates if c.deficit_probability <= target_deficit_probability]
    pool = feasible or candidates
    best = min(pool, key=lambda c: (c.objective_score, c.deficit_probability), default=None)
    ranked = sorted(pool, key=lambda c: (c.objective_score, c.deficit_probability))[:10]
    return {
        "status": "GEOPTIMALISEERD" if feasible else "GEEN ROBUUSTE OPLOSSING",
        "target_deficit_probability": target_deficit_probability,
        "evaluated_candidates": len(candidates),
        "feasible_candidates": len(feasible),
        "best_strategy": asdict(best) if best else {},
        "top_strategies": [asdict(item) for item in ranked],
    }
