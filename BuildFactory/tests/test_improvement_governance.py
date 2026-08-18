from src.improvement_governance import govern_improvement_closure


def test_closes_item_only_with_evidence():
    backlog={"items":[{"id":"IMP-rendering-artifact-pdf","check":"artifact_pdf","status":"IN UITVOERING","progress_percent":70,"recommended_action":"Stabiliseer PDF"}]}
    history=[{"control_status":"GROEN","blocker_count":0},{"control_status":"HERSTELD","blocker_count":0},{"control_status":"GROEN","blocker_count":0}]
    sla={"compliant":True,"release_reliability_score":97.0,"minimum_reliability":95.0}
    improvement={"root_causes":[]}
    result=govern_improvement_closure(backlog,history,sla,improvement,required_stable_runs=3)
    assert result["items"][0]["status"]=="GEREED"
    assert result["items"][0]["progress_percent"]==100


def test_keeps_item_open_if_cause_recurs():
    backlog={"items":[{"id":"IMP-rendering-artifact-pdf","check":"artifact_pdf","status":"OPEN","progress_percent":20}]}
    history=[{"control_status":"GROEN","blocker_count":0}]*3
    sla={"compliant":True,"release_reliability_score":98.0,"minimum_reliability":95.0}
    improvement={"root_causes":[{"check":"artifact_pdf"}]}
    result=govern_improvement_closure(backlog,history,sla,improvement,required_stable_runs=3)
    assert result["items"][0]["status"]=="OPEN"
    assert result["closure_decisions"][0]["decision"]=="KEEP_OPEN"
