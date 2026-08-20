from src.preventive_governance_scenario_optimizer import optimize_preventive_governance_scenarios

P={'plan_id':'P1','actions':[{'recommended_action':'A','expected_effect':{'debt_score_delta':-10,'health_score_delta':5}},{'recommended_action':'B','expected_effect':{'waiver_delta':-1,'health_score_delta':4}}]}
def test_ranks_scenarios():
 x=optimize_preventive_governance_scenarios(P,[{'name':'S1','action_indices':[0],'cost_eur':2000,'feasibility_score':90},{'name':'S2','action_indices':[0,1],'cost_eur':5000,'feasibility_score':80}]); assert x['scenario_count']==2 and x['recommended_scenario'] is not None
def test_budget_penalty():
 x=optimize_preventive_governance_scenarios(P,[{'name':'DUUR','action_indices':[0,1],'cost_eur':10000,'feasibility_score':95}],budget_limit_eur=5000); assert x['status']=='GEEN SCENARIO BINNEN BUDGET'
def test_no_automatic_selection():
 x=optimize_preventive_governance_scenarios(P,[]); assert x['automatic_selection'] is False and x['automatic_execution'] is False
