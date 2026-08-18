from src.alv_decision_workflow import build_alv_workflow

def test_alv_workflow_builds_formal_proposal():
    register={"decisions":[{"id":"DEC-1","reason":"SLA-uitzondering","owner":"Bestuur"}]}
    result=build_alv_workflow(register,{"monthly_per_apartment":25,"reserve_impact":10000})
    assert result["item_count"]==1
    assert result["items"][0]["financial_consequence"]["monthly_per_apartment"]==25.0
    assert result["items"][0]["vote_status"]=="NIET GESTEMD"

def test_alv_workflow_preserves_vote_state():
    register={"decisions":[{"id":"DEC-1","reason":"SLA-uitzondering","owner":"Bestuur"}]}
    existing={"items":[{"decision_id":"DEC-1","agenda_status":"GEREED VOOR ALV","vote_status":"AFGEROND","vote_result":"AANGENOMEN"}]}
    result=build_alv_workflow(register,existing=existing)
    assert result["items"][0]["vote_result"]=="AANGENOMEN"
    assert result["decided_count"]==1
