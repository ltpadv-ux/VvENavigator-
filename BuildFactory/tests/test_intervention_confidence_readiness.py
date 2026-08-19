from src.intervention_confidence_readiness import score_intervention_confidence

def recs():
 return {'status':'BEWIJSGESTUURDE AANBEVELING BESCHIKBAAR','recommendations':[{'intervention':'VROEG INGRIJPEN','similarity_score':90,'avg_effectiveness_score':88,'evidence_strength':'STERK','case_count':5,'ranking_score':91}]}

def test_high_confidence_is_decision_ready():
 x=score_intervention_confidence(recs(),{'data_quality_score':95,'model_consistency_score':92,'scenario_uncertainty_score':10}); assert x['decision_readiness']=='BESLUITRIJP'; assert x['best_recommendation']['confidence_score']>=85

def test_low_evidence_blocks_readiness():
 r=recs(); r['recommendations'][0]['evidence_strength']='BEPERKT'; r['recommendations'][0]['case_count']=1
 x=score_intervention_confidence(r,{'data_quality_score':80,'model_consistency_score':80,'scenario_uncertainty_score':30}); assert x['best_recommendation']['decision_readiness']!='BESLUITRIJP'

def test_no_recommendations_not_ready():
 x=score_intervention_confidence({'status':'ONVOLDOENDE HISTORISCH BEWIJS','recommendations':[]}); assert x['decision_readiness']=='NIET BESLUITRIJP'; assert x['automatic_decision'] is False
