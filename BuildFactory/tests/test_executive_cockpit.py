import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from executive_cockpit import build_executive_cockpit


def test_executive_cockpit_builds_compact_board_view():
    decision = {
        "status": "BESLUITRIJP",
        "readiness_score": 88.5,
        "board_decision": "Kies scenario Duurzaam.",
        "key_metrics": {"deficit_probability": 0.04, "monthly_per_apartment": 210, "scenario": "Duurzaam"},
        "blocking_reasons": [],
    }
    result = build_executive_cockpit(
        decision,
        {"vni": 78.0},
        {"ending_reserve": 125000},
        {"health_score": 95.0},
    )
    assert result["status"] == "BESLUITRIJP"
    assert result["best_strategy"] == "Duurzaam"
    assert result["monthly_per_apartment"] == 210
    assert len(result["top_actions"]) == 3
