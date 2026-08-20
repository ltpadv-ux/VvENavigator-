from src.integrated_financial_governance_decision_cockpit import build_integrated_financial_governance_cockpit

def _base():
 optimizer={'optimizer_id':'O1','ranked_scenarios':[{'scenario_id':'S1','effect_score':90,'feasibility_score':85}]}
 funding={'scenario_funding_impact':[{'scenario_id':'S1','financial_resilience_score':90}]}
 fairness={'scenario_affordability_fairness':[{'scenario_id':'S1','fairness_score':88}]}
 smoothing={'ranked_funding_paths':[{'smoothing_id':'P1','scenario_id':'S1','scenario_name':'GEBALANCEERD','term_months':36,'reserve_share_pct':25,'smoothing_score':92,'reserve_floor_ok':True,'mjop_buffer_ok':True,'maximum_monthly_extra_eur':35,'reserve_after_eur':120000,'mjop_space_after_eur':50000}]}
 stress={'stress_test_id':'T1','ranked_stress_paths':[{'smoothing_id':'P1','stress_resilience_score':86,'stress_status':'STRESS-ROBUUST','stressed_max_monthly_extra_eur':42,'stressed_reserve_after_eur':110000}]}
 return optimizer,funding,fairness,smoothing,stress

def test_integrated_preferred_path():
 x=build_integrated_financial_governance_cockpit(*_base(),{'governance_risk_score':10}); assert x['integrated_preferred_path']['decision_status']=='INTEGRAAL VOORKEURSPAD'

def test_buffer_failure_blocks():
 o,f,fa,s,st=_base(); s['ranked_funding_paths'][0]['mjop_buffer_ok']=False; x=build_integrated_financial_governance_cockpit(o,f,fa,s,st); assert x['integrated_preferred_path']['blocker'] is True

def test_no_automatic_decision():
 x=build_integrated_financial_governance_cockpit(*_base()); assert x['automatic_decision'] is False and x['automatic_execution'] is False
