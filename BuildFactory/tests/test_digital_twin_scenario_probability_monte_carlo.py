from src.digital_twin_scenario_probability_monte_carlo import run_scenario_monte_carlo

def test_monte_carlo_returns_probabilities():
 s={'scenario_name':'BASIS','snapshots':[{'horizon_years':30,'reserve_eur':100000,'cash_eur':50000,'annual_contribution_eur':120000,'operating_cost_eur':60000,'mjop_cost_eur':30000,'risk_cost_eur':5000}]}; x=run_scenario_monte_carlo(s,simulations=200,seed=1); assert 0<=x['probability_reserve_shortfall_pct']<=100 and 0<=x['probability_liquidity_shortfall_pct']<=100

def test_high_shock_increases_risk():
 s={'scenario_name':'SHOCK','snapshots':[{'horizon_years':10,'reserve_eur':10000,'cash_eur':5000,'annual_contribution_eur':20000,'operating_cost_eur':15000,'mjop_cost_eur':5000,'risk_cost_eur':1000}]}; x=run_scenario_monte_carlo(s,simulations=200,seed=2,rules={'annual_adverse_shock_probability':1,'adverse_shock_cost_eur':50000}); assert x['status'] in {'HOOG RISICO','KRITIEK RISICO'}

def test_no_automatic_decision():
 x=run_scenario_monte_carlo({'snapshots':[{'horizon_years':1}]},simulations=100); assert x['automatic_decision'] is False and x['automatic_scenario_selection'] is False
