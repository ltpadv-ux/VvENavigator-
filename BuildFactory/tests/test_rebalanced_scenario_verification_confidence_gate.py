from src.rebalanced_scenario_verification_confidence_gate import verify_rebalanced_scenario

def test_gate_passes_when_all_limits_met():
 r={'rebalancing_id':'R1','projected_within_risk_appetite':True}; m={'monte_carlo_id':'M1','simulations':2000,'probability_reserve_shortfall_pct':4,'probability_liquidity_shortfall_pct':5,'probability_combined_shortfall_pct':2}; x=verify_rebalanced_scenario(r,m,{'max_reserve_shortfall_pct':10,'max_liquidity_shortfall_pct':10,'max_combined_shortfall_pct':5},{'minimum_confidence_pct':95}); assert x['verified_for_board_decision'] is True
def test_gate_blocks_limit_breach():
 r={'projected_within_risk_appetite':False}; m={'simulations':2000,'probability_reserve_shortfall_pct':12,'probability_liquidity_shortfall_pct':5,'probability_combined_shortfall_pct':2}; assert verify_rebalanced_scenario(r,m)['verified_for_board_decision'] is False
def test_no_automatic_activation():
 x=verify_rebalanced_scenario({},{}); assert x['automatic_scenario_activation'] is False and x['automatic_decision'] is False
