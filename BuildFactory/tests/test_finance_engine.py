import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from finance_engine import FinanceYear, annual_contribution_needed, build_cashflow, liquidity_gap


def test_cashflow_rolls_reserve_forward():
    rows = build_cashflow([
        FinanceYear(2026, contribution_income=20000, operating_expenses=12000, reserve_opening=50000),
        FinanceYear(2027, contribution_income=22000, operating_expenses=14000),
    ])
    assert rows[0]["result"] == 8000.0
    assert rows[0]["reserve_closing"] == 58000.0
    assert rows[1]["reserve_opening"] == 58000.0
    assert rows[1]["reserve_closing"] == 66000.0


def test_inflation():
    rows = build_cashflow([FinanceYear(2028, contribution_income=10000, operating_expenses=5000)], 0.04, 2026)
    assert rows[0]["income"] == 10816.0
    assert rows[0]["expenses"] == 5408.0


def test_liquidity_gap_and_contribution():
    assert liquidity_gap(10000, 15000) == 5000.0
    assert annual_contribution_needed(5000, 25, 2) == 100.0
