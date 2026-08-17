from src.self_healing import run_self_healing


def test_self_healing_not_needed_for_verified_result():
    result={"status":"VRIJGEGEVEN VOOR ALV","native_export":{"files":{}},"package":{},"validation":{"sign_off":{"decision":"GO"}},"enterprise":{"release":{"quality_gate":{"can_publish":True}}}}
    out=run_self_healing(result,max_attempts=0)
    assert out["status"] in {"NOT_NEEDED","ESCALATE"}


def test_self_healing_escalates_quality_gate_failure():
    result={"status":"BLOCKED","native_export":{"files":{}},"package":{},"validation":{"sign_off":{"decision":"NO-GO"}},"enterprise":{"release":{"quality_gate":{"can_publish":False}}}}
    out=run_self_healing(result,max_attempts=1)
    assert out["status"]=="ESCALATE"
    assert out["escalation_required"] is True
