from src.executive_digital_twin import build_executive_digital_twin

def baseline():
 return {'overall_vve_health_governance_score':80,'status':'ORANJE','domain_scores':{'financial_health':80,'mjop_health':80,'risk_control':80,'treasury_health':80,'governance_maturity':80,'audit_assurance':80,'decision_execution':80,'improvement_progress':80}}

def test_generates_12_24_36_month_projections():
 x=build_executive_digital_twin(baseline()); assert x['scenario_count']>=4; assert [h['months'] for h in x['projections'][0]['horizons']]==[12,24,36]

def test_custom_positive_scenario_can_improve_score():
 x=build_executive_digital_twin(baseline(),{'TEST':{'inflation_delta':0,'interest_delta':0,'contribution_delta':0.10,'mjop_acceleration':0.10,'sustainability_investment':0.20}}); row=next(r for r in x['projections'] if r['scenario']=='TEST'); assert row['score_36m']>x['baseline_score']

def test_governance_remains_human_controlled():
 x=build_executive_digital_twin(baseline()); assert x['human_decision_required'] is True; assert x['automatic_strategy_change'] is False
