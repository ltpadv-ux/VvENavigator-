from src.digital_twin_scenario_branching_what_if import simulate_digital_twin_scenarios

def base_inputs():
 actuals={'close_id':'C1'}; mjop={'annual_plan':[{'year':1,'cost_eur':1000},{'year':5,'cost_eur':5000},{'year':10,'cost_eur':10000},{'year':30,'cost_eur':20000}]}; finance={'reserve_balance_eur':100000,'cash_balance_eur':30000,'annual_contributions_eur':50000,'annual_operating_cost_eur':30000}; risk={'expected_annual_risk_cost_eur':1000}; governance={'governance_risk_score':10}; assumptions={'base_year':1,'inflation_rate':0.04}; return actuals,mjop,finance,risk,governance,assumptions

def test_default_scenarios_created():
 x=simulate_digital_twin_scenarios(*base_inputs()); assert x['scenario_count']==6 and x['preferred_scenario'] is not None

def test_contribution_increase_improves_long_term_reserve():
 a,m,f,r,g,ass=base_inputs(); scenarios=[{'scenario_id':'BASIS','name':'Basis','assumptions':{}},{'scenario_id':'UP','name':'Up','assumptions':{'annual_contribution_multiplier':1.2}}]; x=simulate_digital_twin_scenarios(a,m,f,r,g,ass,scenarios); rows={z['scenario_id']:z for z in x['ranked_scenarios']}; assert rows['UP']['snapshot_30y']['reserve_eur']>rows['BASIS']['snapshot_30y']['reserve_eur']

def test_no_automatic_selection():
 x=simulate_digital_twin_scenarios(*base_inputs()); assert x['automatic_scenario_selection'] is False and x['automatic_decision'] is False
