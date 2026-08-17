import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from report_engine import build_alv_report, build_board_summary, status_label


def test_status_label():
    assert status_label(80) == "KRITIEK"
    assert status_label(60) == "HOOG"
    assert status_label(30) == "NORMAAL"
    assert status_label(10) == "LAAG"


def test_board_summary_limits_actions():
    summary = build_board_summary(82, 74, 200000, 50000, 31, ["A", "B", "C", "D"])
    assert len(summary["top_actions"]) == 3
    assert summary["metrics"][0]["value"] == 82


def test_alv_report():
    summary = build_board_summary(80, 70, 100000, 25000, 20, ["Reservefonds", "Dak", "Lift"])
    report = build_alv_report(summary)
    assert report["planning_horizon_years"] == 30
    assert report["top_decisions"] == ["Reservefonds", "Dak", "Lift"]
