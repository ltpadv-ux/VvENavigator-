from src.predictive_intervention_optimizer import optimize_predictive_interventions

def os(score=70):
    return {'overall_vve_health_governance_score':score,'status':'ORANJE','domain_scores':{'financial_health':70,'mjop_health':70,'risk_control':70,'treasury_health':70,'governance_maturity':70,'audit_assurance':70,'decision_execution':70,'improvement_progress':70}}

def test_optimizer_returns_ranked_options():
    x=optimize_predictive_interventions(os(),top_n=5)
    assert x['candidate_count']>5
    assert len(x['ranking'])==5
    assert x['ranking'][0]['rank']==1

def test_recommendation_is_advisory_only():
    x=optimize_predictive_interventions(os())
    assert x['human_decision_required'] is True
    assert x['automatic_execution'] is False
    assert x['automatic_financing_commitment'] is False

def test_custom_small_grid():
    grid={'contribution_delta':[0.0,0.05],'mjop_acceleration':[0.0],'financing_share':[0.0],'sustainability_investment':[0.0]}
    x=optimize_predictive_interventions(os(),grid=grid,top_n=2)
    assert x['candidate_count']==2
    assert x['top_count']==2
