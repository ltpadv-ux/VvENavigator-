from src.risk_appetite_breach_remediation_rebalancing import build_rebalancing_plan

def test_builds_actions_for_breach():
 ranking={'risk_appetite_id':'R1','appetite_limits_pct':{'reserve_shortfall':10,'liquidity_shortfall':10,'combined_shortfall':5},'ranked_scenarios':[{'scenario_name':'BASIS','risk_appetite_status':'BUITEN RISICOAPPETIJT','reserve_shortfall_pct':18,'liquidity_shortfall_pct':16,'combined_shortfall_pct':9}]}; finance={'apartments':34,'reserve_balance_eur':200000,'annual_contributions_eur':120000}; x=build_rebalancing_plan(ranking,finance); assert x['actions'] and x['source_scenario']=='BASIS'
def test_empty_results():
 x=build_rebalancing_plan({'ranked_scenarios':[]}); assert x['status']=='GEEN SCENARIORESULTATEN'
def test_no_automatic_changes():
 ranking={'ranked_scenarios':[{'scenario_name':'B','risk_appetite_status':'BINNEN RISICOAPPETIJT'}]}; x=build_rebalancing_plan(ranking); assert x['automatic_rebalancing'] is False and x['automatic_contribution_change'] is False
