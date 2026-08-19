from src.preventive_intervention_simulator import simulate_preventive_interventions

def test_no_alert_no_intervention():
 x=simulate_preventive_interventions({'early_intervention_alerts':[]},{'executive_summary':{}}); assert x['status']=='GEEN PREVENTIEVE INTERVENTIE NODIG'

def test_early_intervention_improves_outlook():
 radar={'early_intervention_alerts':[{'severity':'ORANJE','domain':'treasury_score'}]}
 cc={'executive_summary':{'health_governance_score':78,'risk_score':35}}
 x=simulate_preventive_interventions(radar,cc); assert x['health_score_uplift_vs_no_action']>0; assert x['risk_reduction_vs_no_action']>0

def test_recovery_cost_avoidance_is_positive():
 radar={'early_intervention_alerts':[{'severity':'ROOD','domain':'financial_health'}]}
 cc={'executive_summary':{'health_governance_score':70,'risk_score':45}}
 x=simulate_preventive_interventions(radar,cc); assert x['avoided_recovery_cost']>0; assert x['automatic_intervention'] is False
