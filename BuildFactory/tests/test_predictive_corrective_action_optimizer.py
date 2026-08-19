from src.predictive_corrective_action_optimizer import optimize_corrective_actions

MANDATE={'mandate':{'investment_budget_36m':100000}}

def test_green_requires_no_correction():
 x=optimize_corrective_actions({'status':'GROEN'},MANDATE,{}); assert x['status']=='GEEN CORRECTIE NODIG'; assert x['ranking']==[]

def test_orange_generates_ranked_actions():
 variance={'status':'ORANJE','variances':{'governance_score_variance':-3,'contribution_delta_variance':-0.03,'mjop_acceleration_variance':-0.06,'budget_variance':0}}
 x=optimize_corrective_actions(variance,MANDATE,{'governance_score':72}); assert x['status']=='CORRECTIEVOORSTEL BESCHIKBAAR'; assert len(x['ranking'])==5; assert x['recommended_action']['rank']==1

def test_red_budget_overrun_keeps_human_decision():
 variance={'status':'ROOD','variances':{'governance_score_variance':-8,'contribution_delta_variance':-0.04,'mjop_acceleration_variance':-0.10,'budget_variance':25000}}
 x=optimize_corrective_actions(variance,MANDATE,{'governance_score':65}); assert x['human_decision_required'] is True; assert x['automatic_correction'] is False; assert x['candidate_count']>0
