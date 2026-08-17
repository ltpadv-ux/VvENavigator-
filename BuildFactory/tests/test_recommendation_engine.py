import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from recommendation_engine import explain_strategy


def test_explain_strategy_board_ready():
    result = {
        "best_strategy": {
            "scenario": "Duurzaam",
            "shift_years": 1,
            "annual_contribution": 81600,
            "reserve_buffer": 25000,
            "deficit_probability": 0.04,
            "total_mjop": 600000,
            "sustainability_score": 72,
        },
        "top_strategies": [
            {"scenario": "Duurzaam"},
            {"scenario": "Basis"},
            {"scenario": "Versneld"},
        ],
    }
    advice = explain_strategy(result, apartments=34)
    assert advice["status"] == "ADVIES GEREED"
    assert advice["recommendation"]["confidence"] == "HOOG"
    assert advice["key_metrics"]["monthly_per_apartment"] == 200.0
    assert "Duurzaam" in advice["decision_summary"]


def test_no_strategy_means_no_advice():
    advice = explain_strategy({}, apartments=34)
    assert advice["status"] == "GEEN ADVIES"
