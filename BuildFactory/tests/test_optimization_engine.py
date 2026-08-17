import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from optimization_engine import OptimizationTarget, optimize_financing, optimization_summary
from stress_engine import StressAssumptions


def test_optimizer_finds_solution():
    result = optimize_financing(
        start_year=2026,
        years=5,
        opening_reserve=100000,
        annual_operating_costs=20000,
        mjop_costs={2027: 30000, 2029: 40000},
        initial_annual_contribution=30000,
        apartments=34,
        target=OptimizationTarget(max_deficit_probability=0.20, contribution_step=5000, reserve_buffer_step=10000, max_iterations=6),
        assumptions=StressAssumptions(unexpected_cost_probability=0.0, delay_probability=0.0),
        simulations=100,
        seed=7,
    )
    assert result["status"] in {"GEOPTIMALISEERD", "GEEN OPLOSSING"}
    if result["best"]:
        assert result["best"]["probability_of_deficit"] <= 0.20
        assert result["best"]["monthly_per_apartment"] >= 0
        assert optimization_summary(result)["status"] == "GEOPTIMALISEERD"


def test_optimizer_rejects_invalid_apartments():
    try:
        optimize_financing(2026, 5, 100000, 20000, {}, 30000, 0)
    except ValueError as exc:
        assert "apartments" in str(exc)
    else:
        raise AssertionError("ValueError expected")
