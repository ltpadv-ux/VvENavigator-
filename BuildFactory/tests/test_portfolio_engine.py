import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from portfolio_engine import build_portfolio


def test_portfolio_summary():
    results = [
        ("VvE A", {
            "status": "READY",
            "health": {"status": "HEALTHY", "health_score": 95},
            "release": {
                "quality_gate": {"can_publish": True},
                "dashboard": {"vni": 80, "reserve_fund": 100000, "risk_score": 20},
                "annual_mjop_totals": {2027: 50000, 2028: 120000},
            },
        }),
        ("VvE B", {
            "status": "BLOCKED",
            "health": {"status": "DEGRADED", "health_score": 60},
            "release": {
                "quality_gate": {"can_publish": False},
                "dashboard": {"vni": 55, "reserve_fund": 50000, "risk_score": 70},
                "annual_mjop_totals": {2027: 90000},
            },
        }),
    ]
    summary = build_portfolio(results)
    assert summary["portfolio_count"] == 2
    assert summary["ready_count"] == 1
    assert summary["blocked_count"] == 1
    assert summary["total_investment_need"] == 60000
    assert summary["priority_vves"][0]["name"] == "VvE B"
