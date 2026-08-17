from src.production_orchestrator import _decision_layer

def test_decision_layer_blocks_when_quality_gate_fails():
    result=_decision_layer({"release":{"quality_gate":{"can_publish":False},"dashboard":{}}})
    assert result["status"]=="HERZIEN"
    assert result["readiness_score"]<100
    assert result["blocking_reasons"]
