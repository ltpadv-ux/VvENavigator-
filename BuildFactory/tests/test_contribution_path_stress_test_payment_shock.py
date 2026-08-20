from src.contribution_path_stress_test_payment_shock import stress_test_contribution_paths

S={'optimizer_id':'O1','ranked_funding_paths':[{'smoothing_id':'S1','scenario_name':'GEBALANCEERD','term_months':36,'reserve_share_pct':25,'maximum_monthly_extra_eur':20,'reserve_after_eur':100000,'mjop_space_after_eur':50000,'member_funding_need_eur':12000}]}
def test_robust_under_mild_shocks():
 x=stress_test_contribution_paths(S,{'inflation_pct':2,'unexpected_mjop_cost_eur':1000,'interest_rate_pct':2}); assert x['ranked_stress_paths'][0]['stress_status'] in {'STRESS-ROBUUST','STRESS-AANDACHT'}
def test_heavy_shock_can_fail_buffer():
 x=stress_test_contribution_paths(S,{'unexpected_mjop_cost_eur':200000}); assert x['ranked_stress_paths'][0]['buffer_failure'] is True
def test_no_automatic_decision():
 x=stress_test_contribution_paths(S); assert x['automatic_decision'] is False and x['automatic_financing'] is False
