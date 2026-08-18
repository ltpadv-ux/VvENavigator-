from src.intervention_decision_matrix import build_intervention_decision_matrix

def test_empty_matrix():
    x=build_intervention_decision_matrix({'simulations':[]},{'status':'OP KOERS'})
    assert x['option_count']==0
    assert x['human_decision_required'] is False

def test_ranking_prefers_strong_risk_reduction():
    impact={'simulations':[{'intervention_id':'INT-001','domain':'RISICO','kpi':'12m','decision_authority':'Bestuur','options':[{'option':'A','monthly_delta':5,'mjop_shift_months':0,'risk_score_delta':-15,'horizons':{'30':{'lcc':30000}}},{'option':'B','monthly_delta':0,'mjop_shift_months':12,'risk_score_delta':-5,'horizons':{'30':{'lcc':10000}}}]}]}
    x=build_intervention_decision_matrix(impact,{'status':'BUITEN KOERS'})
    assert x['option_count']==2
    assert x['ranking'][0]['rank']==1
    assert x['preferred_option'] in {'A','B'}
