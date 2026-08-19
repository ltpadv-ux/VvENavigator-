from src.evidence_based_intervention_recommendation import recommend_evidence_based_interventions

def radar():
    return {'early_intervention_alerts':[{'domain':'treasury_score','severity':'ORANJE'}]}

def library():
    return {'recommendations':[
        {'profile':'standaard-vve','risk_type':'treasury_score','intervention':'VROEG INGRIJPEN','case_count':5,'avg_effectiveness_score':92,'avg_value_per_euro':3.5,'avg_health_uplift':8,'avg_risk_reduction':10,'evidence_strength':'STERK'},
        {'profile':'ander','risk_type':'mjop_health','intervention':'VROEG INGRIJPEN','case_count':2,'avg_effectiveness_score':95,'avg_value_per_euro':4.0,'avg_health_uplift':9,'avg_risk_reduction':9,'evidence_strength':'BEPERKT'}]}

def test_no_alert_means_no_recommendation():
    x=recommend_evidence_based_interventions({'early_intervention_alerts':[]},library()); assert x['status']=='GEEN ACTIEVE TRENDWAARSCHUWING'

def test_matching_case_ranks_first():
    x=recommend_evidence_based_interventions(radar(),library(),{'vve_profile':'standaard-vve'}); assert x['best_recommendation']['risk_type']=='treasury_score'; assert x['best_recommendation']['similarity_score']>=90

def test_human_decision_preserved():
    x=recommend_evidence_based_interventions(radar(),library(),{'vve_profile':'standaard-vve'}); assert x['human_decision_required'] is True; assert x['automatic_intervention'] is False
