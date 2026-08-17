import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from decision_intelligence import build_decision_intelligence


def test_decision_intelligence_ready():
    strategy = {
        "status": "GEOPTIMALISEERD",
        "best_strategy": {
            "scenario": "Duurzaam",
            "shift_years": 1,
            "annual_contribution": 81600,
            "reserve_buffer": 20000,
            "deficit_probability": 0.03,
            "total_mjop": 750000,
            "sustainability_score": 65,
        },
        "top_strategies": [],
    }
    result = build_decision_intelligence(
        {"status": "STABIEL"},
        {"risk_level": "BEHEERSBAAR"},
        {"status": "GEOPTIMALISEERD"},
        strategy,
        apartments=34,
    )
    assert result["status"] == "BESLUITRIJP"
    assert result["readiness_score"] == 100.0
    assert "Duurzaam" in result["board_decision"]


def test_decision_intelligence_flags_pressure():
    result = build_decision_intelligence(
        {"status": "ACTIE NODIG"},
        {"risk_level": "KRITIEK"},
        {"status": "GEEN ROBUUSTE OPLOSSING"},
        {"status": "GEEN ROBUUSTE OPLOSSING", "best_strategy": {}},
        apartments=34,
    )
    assert result["status"] == "HERZIEN"
    assert result["readiness_score"] < 50
    assert result["blocking_reasons"]
