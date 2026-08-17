import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from mjop_engine import MJOPComponent, annual_totals, generate_plan, reserve_gap


def test_generate_plan_indexes_cost_and_priority():
    item = MJOPComponent(
        "Gevel schilderwerk",
        "Gevel",
        500,
        "m2",
        35,
        6,
        2026,
        condition_score=4,
        risk_score=80,
        urgency=60,
        budget_impact=50,
    )
    plan = generate_plan([item], 2026, horizon_years=10, inflation_rate=0.04)
    assert [row["year"] for row in plan] == [2032, 2038]
    assert plan[0]["base_cost"] == 17500.0
    assert plan[0]["indexed_cost"] == 22575.57
    assert plan[0]["priority"] == 69.0


def test_annual_totals_and_reserve_gap():
    item = MJOPComponent("Lift", "Installaties", 1, "stuk", 12000, 5, 2025)
    plan = generate_plan([item], 2026, horizon_years=10, inflation_rate=0.0)
    assert annual_totals(plan) == {2030: 12000.0, 2035: 12000.0}
    assert reserve_gap(15000, plan, 2030) == 3000.0


def test_invalid_condition_score():
    try:
        MJOPComponent("Dak", "Dak", 100, "m2", 20, 10, 2026, condition_score=7)
    except ValueError as exc:
        assert "condition_score" in str(exc)
    else:
        raise AssertionError("invalid condition score must fail")
