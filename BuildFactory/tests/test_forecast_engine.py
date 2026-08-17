import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from forecast_engine import forecast_signals, forecast_summary, pressure_score, warning_level


def test_warning_levels():
    assert warning_level(80) == "KRITIEK"
    assert warning_level(55) == "WAARSCHUWING"
    assert warning_level(30) == "AANDACHT"
    assert warning_level(10) == "STABIEL"


def test_forecast_detects_reserve_pressure():
    projection = [
        {"year": 2026, "reserve_closing": 120000, "mjop_costs": 10000},
        {"year": 2027, "reserve_closing": 40000, "mjop_costs": 90000},
        {"year": 2028, "reserve_closing": -10000, "mjop_costs": 20000},
    ]
    signals = forecast_signals(projection, {2027: 90000, 2028: 20000}, {2027: 60, 2028: 70}, reserve_floor=50000)
    assert signals[1]["level"] in {"WAARSCHUWING", "KRITIEK"}
    assert signals[2]["message"].startswith("Reserve wordt negatief")
    summary = forecast_summary(signals, 3)
    assert summary["status"] == "ACTIE NODIG"
    assert summary["first_critical_year"] in {2027, 2028}


def test_pressure_score_range():
    score = pressure_score(100000, 10000, 20, 50000)
    assert 0 <= score <= 100
