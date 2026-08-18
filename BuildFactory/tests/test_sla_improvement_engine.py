from src.sla_improvement_engine import analyze_sla_root_causes


def test_root_cause_prioritizes_recurring_quality_issue():
    history=[
        {"control_status":"GEBLOKKEERD","quality_issue_count":2,"repair_count":0},
        {"control_status":"GEBLOKKEERD","quality_issue_count":1,"repair_count":0},
    ]
    diagnostics=[
        {"diagnostics":[{"check":"quality_gate","module":"Compliance & Quality Engine"}]},
        {"diagnostics":[{"check":"quality_gate","module":"Compliance & Quality Engine"}]},
    ]
    result=analyze_sla_root_causes(history,diagnostics)
    assert result["status"]=="IMPROVEMENT_REQUIRED"
    assert result["dominant_root_cause"]["check"]=="quality_gate"
    assert result["improvement_priority"]=="HOOG"


def test_no_structural_issue_when_history_is_green():
    result=analyze_sla_root_causes([{"control_status":"GROEN","quality_issue_count":0,"repair_count":0}],[])
    assert result["status"]=="NO_STRUCTURAL_ISSUE"
