from src.predictive_decision_portfolio import build_predictive_decision_portfolio

def sample():
    return {'ranking':[
      {'rank':1,'intervention':{'contribution_delta':0.05,'mjop_acceleration':0.10,'financing_share':0.25,'sustainability_investment':0.10},'score_36m':86,'estimated_36m_cost':120000},
      {'rank':2,'intervention':{'contribution_delta':0.03,'mjop_acceleration':0.05,'financing_share':0.00,'sustainability_investment':0.00},'score_36m':80,'estimated_36m_cost':50000},
      {'rank':3,'intervention':{'contribution_delta':0.08,'mjop_acceleration':0.20,'financing_share':0.50,'sustainability_investment':0.30},'score_36m':92,'estimated_36m_cost':220000}
    ]}

def test_builds_pareto_frontier():
    x=build_predictive_decision_portfolio(sample()); assert x['pareto_count']>=2; assert x['human_decision_required'] is True

def test_choice_cards_are_unique():
    x=build_predictive_decision_portfolio(sample()); keys=[str(i['intervention']) for i in x['board_choice_cards']]; assert len(keys)==len(set(keys))

def test_no_auto_selection():
    x=build_predictive_decision_portfolio(sample()); assert x['automatic_selection'] is False
