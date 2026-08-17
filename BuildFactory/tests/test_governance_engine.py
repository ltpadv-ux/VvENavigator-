import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from governance_engine import build_alv_agenda, governance_summary, proposal_from_decision, status_from_priority


def test_status_mapping():
    assert status_from_priority("NU") == "BESLUIT NODIG"
    assert status_from_priority("HOOG") == "VOORBEREIDEN"
    assert status_from_priority("PLANNEN") == "AGENDEREN"
    assert status_from_priority("MONITOREN") == "VOLGEN"


def test_proposal_from_decision():
    decision = {
        "action": "Dakbedekking: opnemen in eerstvolgende begroting",
        "priority": "HOOG",
        "horizon": "1-2 jaar",
        "rationale": "Risico 60/100, conditie 4/6.",
    }
    proposal = proposal_from_decision(decision, 50000)
    assert proposal.agenda_item == "Besluit Dakbedekking"
    assert proposal.financial_impact == 50000
    assert proposal.status == "VOORBEREIDEN"


def test_agenda_and_summary():
    decisions = [
        {"action": "Lift: nu uitvoeren", "priority": "NU", "horizon": "0-1 jaar", "rationale": "hoog risico"},
        {"action": "Gevel: planmatig reserveren", "priority": "PLANNEN", "horizon": "2-5 jaar", "rationale": "middel risico"},
    ]
    agenda = build_alv_agenda(decisions, {"Lift": 25000, "Gevel": 40000})
    summary = governance_summary(agenda)
    assert len(agenda) == 2
    assert summary["decision_needed"] == 1
    assert summary["planned"] == 1
    assert summary["total_financial_impact"] == 65000
