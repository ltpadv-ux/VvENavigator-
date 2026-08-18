from datetime import date
from src.mandate_compliance import evaluate_mandate_compliance

def test_budget_overrun_blocks_mandate():
    mandates={"mandates":[{"mandate_id":"MAN-1","decision_id":"DEC-1","owner":"Bestuur","mandate_text":"Voer uit","budget":1000,"spent_amount":1200,"deadline":"2099-01-01","status":"IN UITVOERING"}]}
    result=evaluate_mandate_compliance(mandates,today=date(2026,8,18))
    assert result["status"]=="GEBLOKKEERD"
    assert result["human_escalation_required"] is True

def test_deadline_and_budget_within_mandate_is_green():
    mandates={"mandates":[{"mandate_id":"MAN-2","decision_id":"DEC-2","owner":"Beheerder","mandate_text":"Voer uit","budget":1000,"spent_amount":500,"deadline":"2099-01-01","status":"IN UITVOERING"}]}
    result=evaluate_mandate_compliance(mandates,today=date(2026,8,18))
    assert result["status"]=="BINNEN MANDAAT"
    assert result["red_count"]==0
