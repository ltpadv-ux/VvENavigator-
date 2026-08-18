from src.reliability_sla import evaluate_reliability_sla


def test_sla_compliant():
    trend={"release_reliability_score":97.5,"runs":8,"blocked_runs":0,"trend":"STABIEL"}
    result=evaluate_reliability_sla(trend,minimum_reliability=95.0,max_blocked_recent=1)
    assert result["status"]=="BINNEN SLA"
    assert result["compliant"] is True


def test_sla_breach():
    trend={"release_reliability_score":88.0,"runs":5,"blocked_runs":2,"trend":"VERSLECHTEREND"}
    result=evaluate_reliability_sla(trend,minimum_reliability=95.0,max_blocked_recent=1)
    assert result["status"]=="SLA BREACH"
    assert result["compliant"] is False
    assert len(result["issues"])>=2
