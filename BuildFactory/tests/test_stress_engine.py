import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from stress_engine import StressAssumptions, run_monte_carlo, stress_risk_level, stress_summary


def test_monte_carlo_is_reproducible_and_bounded():
    result = run_monte_carlo(
        2026,
        5,
        100000,
        30000,
        20000,
        {2027: 25000, 2029: 50000},
        simulations=200,
        seed=7,
    )
    assert result["simulations"] == 200
    assert 0.0 <= result["probability_of_deficit"] <= 1.0
    assert result["ending_reserve_p10"] <= result["ending_reserve_p50"] <= result["ending_reserve_p90"]


def test_high_stress_creates_material_deficit_probability():
    assumptions = StressAssumptions(
        inflation_mean=0.06,
        inflation_std=0.01,
        cost_overrun_mean=0.25,
        cost_overrun_std=0.03,
        delay_probability=0.0,
        unexpected_cost_probability=0.5,
        unexpected_cost_fraction=0.25,
    )
    result = run_monte_carlo(
        2026, 4, 10000, 5000, 8000, {2026: 20000, 2028: 30000},
        simulations=200, assumptions=assumptions, seed=3,
    )
    assert result["probability_of_deficit"] > 0.5
    assert result["risk_level"] == "KRITIEK"


def test_risk_labels_and_summary():
    assert stress_risk_level(0.05) == "BEHEERSBAAR"
    assert stress_risk_level(0.15) == "AANDACHT"
    assert stress_risk_level(0.30) == "HOOG"
    assert stress_risk_level(0.60) == "KRITIEK"
    summary = stress_summary([
        {"probability_of_deficit": 0.6, "risk_level": "KRITIEK"},
        {"probability_of_deficit": 0.3, "risk_level": "HOOG"},
    ])
    assert summary["runs"] == 2
    assert summary["critical"] == 1
    assert summary["high"] == 1
