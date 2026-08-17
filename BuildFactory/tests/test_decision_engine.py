import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from decision_engine import advise_component, board_decisions, decision_score, priority_label


def test_priority_labels():
    assert priority_label(80) == "NU"
    assert priority_label(60) == "HOOG"
    assert priority_label(30) == "PLANNEN"
    assert priority_label(10) == "MONITOREN"


def test_advise_component_sustainability():
    decision = advise_component("Dak", 80, 5, 10000, 20000, sustainability_gain=20)
    assert decision.priority in {"NU", "HOOG"}
    assert "verduurzaming" in decision.action


def test_board_decisions_ranked():
    items = [
        {"component": "Lift", "risk_score": 80, "condition_score": 5, "liquidity_gap": 5000, "annual_mjop": 10000},
        {"component": "Gevel", "risk_score": 20, "condition_score": 2, "liquidity_gap": 0, "annual_mjop": 10000},
    ]
    decisions = board_decisions(items, top_n=2)
    assert decisions[0]["score"] >= decisions[1]["score"]
    assert decisions[0]["action"].startswith("Lift")


def test_decision_score_validates_condition():
    try:
        decision_score(50, 7, 0, 10000)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid condition score must fail")
