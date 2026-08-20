from src.scenario_activation_baseline_monitoring_covenant import activate_scenario_baseline, monitor_actuals_against_baseline

def test_activation_freezes_baseline():
 v={'validated_for_manual_activation':True,'activation_mandate':{'mandate_id':'M1','scenario_name':'BASIS','risk_appetite_limits_pct':{'reserve':10,'liquidity':10,'combined':5},'verified_shortfall_pct':{'reserve':4,'liquidity':3,'combined':2},'simulation_confidence_pct':97,'execution_owner':'Bestuur','activation_date':'2026-09-01'}}; s={'scenario_id':'S1','scenario_name':'BASIS','snapshots':[{'horizon_years':1,'reserve_eur':1000,'cash_eur':500,'annual_contribution_eur':1200,'mjop_cost_eur':100}]}; a={'manual_activation_confirmed':True,'activated_by':'Bestuur','activated_at':'2026-09-01T09:00'}; x=activate_scenario_baseline(v,s,a); assert x['active'] is True and x['baseline_freeze']['frozen'] is True

def test_monitoring_detects_material_variance():
 ar={'activation_id':'A1','baseline_freeze':{'risk_appetite_limits_pct':{'reserve':10,'liquidity':10,'combined':5},'snapshots':[{'horizon_years':1,'reserve_eur':1000,'cash_eur':500,'annual_contribution_eur':1200,'mjop_cost_eur':100}]},'monitoring_covenant':{'material_variance_pct':5}}; y=monitor_actuals_against_baseline(ar,{'horizon_years':1,'reserve_eur':900,'cash_eur':500,'annual_contribution_eur':1200,'mjop_cost_eur':100}); assert y['requires_board_review'] is True

def test_no_automatic_baseline_change():
 x=activate_scenario_baseline({}, {}, {}); assert x['automatic_baseline_change'] is False and x['automatic_activation'] is False
