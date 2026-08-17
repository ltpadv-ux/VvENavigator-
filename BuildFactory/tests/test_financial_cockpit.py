import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from financial_cockpit import (
    FinancialAssumptions,
    cockpit_summary,
    project_reserve,
    required_contribution_for_nonnegative_reserve,
)


def test_projection_and_summary():
    projection = project_reserve(
        2026,
        3,
        100000,
        {2027: 25000},
        FinancialAssumptions(12000, 6000, 0.0, 0.0, 0.0),
    )
    assert projection[0]["reserve_closing"] == 106000.0
    assert projection[1]["reserve_closing"] == 87000.0
    summary = cockpit_summary(projection, 34)
    assert summary["status"] == "VOLDOENDE"
    assert summary["apartments"] == 34


def test_required_contribution():
    result = required_contribution_for_nonnegative_reserve(
        2026,
        5,
        0,
        {2026: 10000, 2028: 10000},
        5000,
        10,
        growth=0.0,
    )
    assert result["annual_contribution_total"] >= 9000
    assert result["monthly_per_apartment"] > 0
