from src.explainable_governance_ai import explain_governance_recommendations

def test_no_recommendations_no_explanation():
 x=explain_governance_recommendations({'recommendations':[]},{})
 assert x['status']=='GEEN UITLEG BESCHIKBAAR'; assert x['automatic_decision'] is False

def test_explanation_contains_drivers_and_uncertainties():
 c={'decision_readiness':'NADER ONDERZOEK','intervention_confidence_readiness_version':'10.9.0','recommendations':[{'intervention':'VROEG INGRIJPEN','ranking_score':82,'confidence_score':74,'similarity_score':65,'avg_effectiveness_score':85,'evidence_strength':'BEPERKT','case_count':2,'decision_readiness':'NADER ONDERZOEK','confidence_components':{'data_quality':75,'model_consistency':80,'scenario_uncertainty':60}}]}
 x=explain_governance_recommendations(c,{'evidence_based_intervention_recommendation_version':'10.8.0'})
 assert x['status']=='UITLEG BESCHIKBAAR'; assert x['best_explanation']['decisive_drivers']; assert x['best_explanation']['uncertainties']

def test_alternatives_are_explained():
 recs=[{'intervention':'A','ranking_score':90,'confidence_score':88,'similarity_score':90,'avg_effectiveness_score':90,'evidence_strength':'STERK','case_count':5,'decision_readiness':'BESLUITRIJP','confidence_components':{'data_quality':90,'model_consistency':90,'scenario_uncertainty':90}},{'intervention':'B','ranking_score':70,'confidence_score':72,'similarity_score':60,'avg_effectiveness_score':80,'evidence_strength':'REDELIJK','case_count':3,'decision_readiness':'NADER ONDERZOEK','confidence_components':{'data_quality':90,'model_consistency':75,'scenario_uncertainty':80}}]
 x=explain_governance_recommendations({'decision_readiness':'BESLUITRIJP','recommendations':recs},{})
 assert x['best_explanation']['alternatives_considered'][0]['intervention']=='B'
