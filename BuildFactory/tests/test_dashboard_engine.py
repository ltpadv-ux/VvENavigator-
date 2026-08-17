import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from dashboard_engine import DashboardInput, build_dashboard, mgi_score, reserve_score, vni_score


def test_scores():
    data = DashboardInput(
        reserve_fund=80000,
        required_reserve=100000,
        annual_mjop=20000,
        annual_budget=30000,
        risk_score=20,
        condition_score=2,
    )
    assert reserve_score(80000, 100000) == 80.0
    assert mgi_score(20000, 30000) == 33.33
    assert vni_score(data) == 68.83


def test_dashboard_top_three_actions():
    data = DashboardInput(100000, 100000, 10000, 30000, 10, 2)
    result = build_dashboard(data, [
        {"component": "Dak", "priority": 40},
        {"component": "Gevel", "priority": 90},
        {"component": "Lift", "priority": 60},
        {"component": "Schilderwerk", "priority": 30},
    ])
    assert [x["component"] for x in result["top_3_actions"]] == ["Gevel", "Lift", "Dak"]
    assert result["vni_status"] in {"GROEN", "GEEL", "ORANJE", "ROOD"}
