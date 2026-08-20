from src.contribution_smoothing_multi_year_funding_optimizer import optimize_contribution_smoothing

F={'funding_id':'F1','apartments':34,'scenario_funding_impact':[{'scenario_id':'S1','name':'GEBALANCEERD','funding_gap_eur':12000,'cost_eur':12000}]}
FIN={'reserve_fund_eur':100000,'minimum_reserve_eur':80000,'mjop_available_space_eur':30000}

def test_smoothing_generates_ranked_paths():
 x=optimize_contribution_smoothing(F,FIN,terms_months=[12,24],reserve_shares=[0,0.5]); assert x['option_count']==4 and x['recommended_funding_path'] is not None

def test_reserve_floor_is_protected():
 x=optimize_contribution_smoothing(F,FIN,terms_months=[12],reserve_shares=[1.0]); r=x['ranked_funding_paths'][0]; assert r['reserve_after_eur']>=80000

def test_no_automatic_financial_actions():
 x=optimize_contribution_smoothing(F,FIN); assert x['automatic_contribution_change'] is False and x['automatic_reserve_draw'] is False and x['automatic_financing'] is False
