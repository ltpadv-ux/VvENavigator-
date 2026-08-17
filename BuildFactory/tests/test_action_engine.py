import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from action_engine import build_action, execution_summary


def test_action_budget_and_light():
    row = build_action("Lift revisie", "Technisch beheer", "2027-06-30", 25000, 10000, 40, "VERTRAAGD")
    assert row["budget_variance"] == 15000
    assert row["traffic_light"] == "ORANJE"


def test_action_over_budget_is_red():
    row = build_action("Dak", "Bestuur", "2028-01-01", 10000, 12000, 80, "LOPEND")
    assert row["traffic_light"] == "ROOD"


def test_execution_summary():
    actions = [
        build_action("A", "X", "2027-01-01", 10000, 5000, 100, "GEREED"),
        build_action("B", "Y", "2027-01-01", 20000, 5000, 20, "OPEN"),
    ]
    result = execution_summary(actions)
    assert result["actions"] == 2
    assert result["total_budget"] == 30000
    assert result["total_spent"] == 10000
    assert result["traffic_lights"]["GROEN"] == 1
