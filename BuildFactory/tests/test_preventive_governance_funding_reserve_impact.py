from src.preventive_governance_funding_reserve_impact import assess_funding_reserve_impact

def test_robust_scenario():
 o={'optimizer_id':'O1','ranked_scenarios':[{'scenario_id':'S1','name':'MINIMAAL','cost_eur':5000,'optimization_score':80,'threshold_shift_runs':2}]}
 f={'reserve_fund_eur':100000,'liquidity_eur':120000,'mjop_available_space_eur':20000,'minimum_reserve_eur':50000}
 x=assess_funding_reserve_impact(o,f,34); assert x['scenario_funding_impact'][0]['funding_status']=='FINANCIEEL ROBUUST'

def test_extra_contribution_calculated_when_floor_breached():
 o={'ranked_scenarios':[{'scenario_id':'S1','name':'VERSNELD','cost_eur':60000}]}
 f={'reserve_fund_eur':70000,'liquidity_eur':70000,'mjop_available_space_eur':100000,'minimum_reserve_eur':30000}
 x=assess_funding_reserve_impact(o,f,20); assert x['scenario_funding_impact'][0]['extra_contribution_per_apartment_eur']>0

def test_no_automatic_financing():
 x=assess_funding_reserve_impact({'ranked_scenarios':[]},{},34); assert x['automatic_funding'] is False and x['automatic_contribution_change'] is False
