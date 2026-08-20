from src.probability_aware_scenario_risk_appetite import rank_probability_aware_scenarios

def test_within_appetite_ranks_first():
 rows=[{'scenario_name':'A','probability_reserve_shortfall_pct':4,'probability_liquidity_shortfall_pct':5,'probability_combined_shortfall_pct':2,'ending_reserve_distribution_eur':{'p05':10000,'p50':50000},'ending_cash_distribution_eur':{'p50':20000},'deterministic_score':80},{'scenario_name':'B','probability_reserve_shortfall_pct':20,'probability_liquidity_shortfall_pct':18,'probability_combined_shortfall_pct':10,'ending_reserve_distribution_eur':{'p05':-5000,'p50':60000},'ending_cash_distribution_eur':{'p50':10000},'deterministic_score':90}]; x=rank_probability_aware_scenarios(rows); assert x['preferred_scenario']['scenario_name']=='A'
def test_custom_appetite_limits():
 rows=[{'scenario_name':'A','probability_reserve_shortfall_pct':8,'probability_liquidity_shortfall_pct':8,'probability_combined_shortfall_pct':4}]; x=rank_probability_aware_scenarios(rows,{'max_reserve_shortfall_pct':5,'max_liquidity_shortfall_pct':10,'max_combined_shortfall_pct':5}); assert 'RESERVE_SHORTFALL' in x['ranked_scenarios'][0]['breaches']
def test_no_automatic_selection():
 x=rank_probability_aware_scenarios([]); assert x['automatic_scenario_selection'] is False and x['automatic_decision'] is False
