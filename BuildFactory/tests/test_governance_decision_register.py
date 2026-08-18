from src.governance_decision_register import build_decision_register

def test_register_creates_human_decision():
    auto={"cycle_status":"MENSELIJK BESLUIT VEREIST","release_status":"GEBLOKKEERD","sla_compliant":False,"next_action":"Beoordelen","human_decision_gates":[{"gate":"SLA_EXCEPTION","owner":"Product owner","reason":"SLA breach"}]}
    result=build_decision_register(auto)
    assert result["dashboard"]["open_decisions"]==1
    assert result["decisions"][0]["status"]=="OPEN"
    assert result["audit_hash"]

def test_register_preserves_recorded_decision():
    auto={"cycle_status":"MENSELIJK BESLUIT VEREIST","human_decision_gates":[{"gate":"SLA_EXCEPTION","owner":"Product owner","reason":"SLA breach"}]}
    first=build_decision_register(auto); first["decisions"][0].update(status="BESLOTEN",decision="ACCEPTEREN",rationale="Tijdelijke uitzondering")
    second=build_decision_register(auto,first)
    assert second["decisions"][0]["decision"]=="ACCEPTEREN"
    assert second["dashboard"]["open_decisions"]==0
