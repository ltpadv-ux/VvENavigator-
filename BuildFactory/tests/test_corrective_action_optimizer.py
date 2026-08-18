from src.corrective_action_optimizer import optimize_corrective_actions

def test_optimizer_recommends_scope_or_planning_action():
    forecast={"forecasts":[{"mandate_id":"MAN-1","risk":"HOOG","budget":100000,"projected_final_cost":120000,"progress_percent":50,"deadline":"2026-09-01"}]}
    result=optimize_corrective_actions(forecast)
    assert result["recommendation_count"]==1
    assert result["recommendations"][0]["recommended_action"]["action"] in {"SCOPE_AANPASSEN","PLANNING_AANPASSEN"}

def test_optimizer_no_action_when_stable():
    result=optimize_corrective_actions({"forecasts":[{"mandate_id":"MAN-2","risk":"LAAG"}]})
    assert result["status"]=="GEEN ACTIE NODIG"
