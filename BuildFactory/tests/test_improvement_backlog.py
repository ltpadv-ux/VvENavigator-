from src.improvement_backlog import build_improvement_backlog


def test_backlog_prioritizes_high_impact_items_and_preserves_owner():
    improvement={"root_causes":[
        {"category":"Rendering","check":"artifact_pdf","occurrences":2,"impact_score":8,"priority":"HOOG","recommended_action":"Stabiliseer PDF"},
        {"category":"Packaging","check":"distribution_zip","occurrences":1,"impact_score":3,"priority":"MIDDEL","recommended_action":"Herstel packaging"},
    ]}
    existing=[{"id":"IMP-rendering-artifact_pdf","owner":"Louis","status":"IN UITVOERING","progress_percent":40,"created_at":"2026-01-01T00:00:00+00:00"}]
    result=build_improvement_backlog(improvement,existing)
    assert result["items"][0]["priority"]=="HOOG"
    assert result["items"][0]["owner"]=="Louis"
    assert result["items"][0]["progress_percent"]==40
    assert result["high_priority_open"]==1
