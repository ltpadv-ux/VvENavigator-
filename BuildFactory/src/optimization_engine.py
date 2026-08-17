"""Optimization engine for VvE Navigator contribution and reserve planning."""
from __future__ import annotations

from dataclasses import dataclass, asdict

from stress_engine import StressAssumptions, run_monte_carlo


@dataclass(frozen=True)
class OptimizationTarget:
    max_deficit_probability: float = 0.05
    contribution_step: float = 1000.0
    reserve_buffer_step: float = 5000.0
    max_iterations: int = 60


def optimize_financing(
    start_year: int,
    years: int,
    opening_reserve: float,
    annual_operating_costs: float,
    mjop_costs: dict[int, float],
    initial_annual_contribution: float,
    apartments: int,
    target: OptimizationTarget | None = None,
    assumptions: StressAssumptions | None = None,
    simulations: int = 500,
    seed: int = 42,
) -> dict:
    """Find a low-cost contribution/reserve combination meeting a deficit-risk target."""
    if apartments <= 0:
        raise ValueError("apartments must be positive")
    if initial_annual_contribution < 0 or opening_reserve < 0:
        raise ValueError("contribution and reserve must be non-negative")
    target = target or OptimizationTarget()
    if not 0 <= target.max_deficit_probability < 1:
        raise ValueError("max_deficit_probability must be between 0 and 1")

    best: dict | None = None
    candidates: list[dict] = []

    for reserve_i in range(target.max_iterations):
        reserve_buffer = reserve_i * target.reserve_buffer_step
        contribution = initial_annual_contribution
        for contribution_i in range(target.max_iterations):
            result = run_monte_carlo(
                start_year=start_year,
                years=years,
                opening_reserve=opening_reserve + reserve_buffer,
                annual_contribution=contribution,
                annual_operating_costs=annual_operating_costs,
                mjop_costs=mjop_costs,
                simulations=simulations,
                assumptions=assumptions,
                seed=seed,
            )
            probability = float(result["probability_of_deficit"])
            candidate = {
                "annual_contribution": round(contribution, 2),
                "extra_reserve_buffer": round(reserve_buffer, 2),
                "probability_of_deficit": probability,
                "monthly_per_apartment": round(contribution / apartments / 12, 2),
                "objective_cost": round(contribution * years + reserve_buffer, 2),
                "risk_level": result["risk_level"],
            }
            candidates.append(candidate)
            if probability <= target.max_deficit_probability:
                if best is None or candidate["objective_cost"] < best["objective_cost"]:
                    best = candidate
                break
            contribution += target.contribution_step

    return {
        "status": "GEOPTIMALISEERD" if best else "GEEN OPLOSSING",
        "target": asdict(target),
        "best": best or {},
        "tested_candidates": len(candidates),
        "candidate_preview": sorted(candidates, key=lambda x: (x["objective_cost"], x["probability_of_deficit"]))[:10],
    }


def optimization_summary(result: dict) -> dict:
    best = result.get("best", {})
    if not best:
        return {"status": "GEEN OPLOSSING", "advies": "Verhoog zoekruimte of herijk MJOP/scenario's"}
    return {
        "status": result.get("status", "GEOPTIMALISEERD"),
        "annual_contribution": best["annual_contribution"],
        "monthly_per_apartment": best["monthly_per_apartment"],
        "extra_reserve_buffer": best["extra_reserve_buffer"],
        "probability_of_deficit": best["probability_of_deficit"],
        "advies": "Gebruik deze combinatie als minimum robuuste financieringsroute",
    }
