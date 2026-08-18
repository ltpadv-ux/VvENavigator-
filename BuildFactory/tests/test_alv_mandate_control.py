from src.alv_mandate_control import build_execution_mandates

def test_only_approved_decisions_create_mandates():
    workflow={"items":[{"decision_id":"DEC-1","vote_status":"AFGEROND","vote_result":"AANGENOMEN","owner":"Bestuur","execution_order":"Voer uit","financial_consequence":{"reserve_impact":10000}},{"decision_id":"DEC-2","vote_status":"NIET GESTEMD","vote_result":"ONBEKEND"}]}
    result=build_execution_mandates(workflow)
    assert result["mandate_count"]==1
    assert result["mandates"][0]["decision_id"]=="DEC-1"
    assert result["total_budget"]==10000

def test_existing_progress_is_preserved():
    workflow={"items":[{"decision_id":"DEC-1","vote_status":"AFGEROND","vote_result":"AANGENOMEN","owner":"Bestuur","execution_order":"Voer uit","financial_consequence":{"reserve_impact":10000}}]}
    existing={"mandates":[{"decision_id":"DEC-1","mandate_id":"MAN-X","progress_percent":40,"spent_amount":2500,"status":"IN UITVOERING","budget":10000}]}
    result=build_execution_mandates(workflow,existing)
    assert result["mandates"][0]["progress_percent"]==40
    assert result["budget_remaining"]==7500
