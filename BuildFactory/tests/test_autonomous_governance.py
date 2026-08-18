from src.autonomous_governance import build_governance_cycle

def test_autonomous_green_cycle():
    report={"control_center":{"status":"GROEN"},"reliability_sla":{"compliant":True},"improvement_governance":{"open_count":0,"status":"ALL_CLOSED"},"diagnostics":{"blocking_count":0}}
    result=build_governance_cycle(report)
    assert result["cycle_status"]=="AUTONOOM GROEN"
    assert result["human_decision_gates"]==[]

def test_human_gate_for_blocked_release():
    report={"control_center":{"status":"GEBLOKKEERD"},"reliability_sla":{"compliant":False},"improvement_governance":{"open_count":1,"status":"GOVERNED"},"diagnostics":{"blocking_count":1}}
    result=build_governance_cycle(report)
    assert result["cycle_status"]=="MENSELIJK BESLUIT VEREIST"
    assert len(result["human_decision_gates"])>=2
