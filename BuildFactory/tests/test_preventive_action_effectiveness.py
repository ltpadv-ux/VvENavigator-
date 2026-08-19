from src.preventive_action_effectiveness import verify_preventive_action_effectiveness

def mandate():
 return {'status':'VROEG-ACTIEMANDAAT ACTIEF','mandate':{'mandate_id':'PEAM-1','target_health_score':82,'target_risk_score':20,'budget':18000,'expected_avoided_recovery_cost':30000,'progress_pct':100,'evidence':['bewijs']}}

def test_effect_proven():
 a={'health_governance_score':84,'risk_score':18,'actual_spend':16000,'progress_pct':100,'evidence':['bewijs'],'counterfactual_recovery_cost':46000,'trend_turned':True}
 b={'health_governance_score':78,'risk_score':25}
 x=verify_preventive_action_effectiveness(mandate(),a,b); assert x['status']=='PREVENTIEF EFFECT BEWEZEN'; assert x['verification']['verified_avoided_recovery_cost']==30000

def test_missing_evidence_blocks_proof():
 a={'health_governance_score':84,'risk_score':18,'actual_spend':16000,'progress_pct':100,'evidence':[],'counterfactual_recovery_cost':46000,'trend_turned':True}
 x=verify_preventive_action_effectiveness(mandate(),a,{'health_governance_score':78,'risk_score':25}); assert x['status']!='PREVENTIEF EFFECT BEWEZEN'; assert x['checks']['execution_complete'] is False

def test_no_active_mandate():
 x=verify_preventive_action_effectiveness({},{}); assert x['status']=='GEEN ACTIEF PREVENTIEF MANDAAT'
