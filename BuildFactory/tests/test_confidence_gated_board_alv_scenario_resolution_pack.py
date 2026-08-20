from src.confidence_gated_board_alv_scenario_resolution_pack import build_confidence_gated_resolution_pack

def test_gate_required():
 gate={'verified_for_board_decision':False,'status':'CONFIDENCE GATE GEBLOKKEERD','blockers':['x']}; x=build_confidence_gated_resolution_pack(gate,{},{}); assert 'GEBLOKKEERD' in x['status']
def test_pack_contains_mc_and_horizons():
 gate={'verified_for_board_decision':True,'status':'CONFIDENCE GATE GESLAAGD','confidence_gate_id':'G1','simulation_confidence_pct':97.7,'risk_appetite_limits_pct':{'reserve':10,'liquidity':10,'combined':5},'verified_shortfall_pct':{'reserve':4,'liquidity':5,'combined':2}}
 scenario={'scenario_name':'BASIS','snapshots':[{'horizon_years':5,'reserve_eur':1,'cash_eur':2,'financial_health_score':80,'status':'ROBUUST'},{'horizon_years':10},{'horizon_years':30}]}; mc={'monte_carlo_id':'M1','simulations':2000}; x=build_confidence_gated_resolution_pack(gate,scenario,mc); assert len(x['horizon_impacts'])==3 and x['monte_carlo_evidence']['simulations']==2000
def test_no_automatic_adoption():
 gate={'verified_for_board_decision':True,'status':'CONFIDENCE GATE GESLAAGD'}; x=build_confidence_gated_resolution_pack(gate,{'scenario_name':'X'},{}); assert x['automatic_resolution_adoption'] is False and x['automatic_decision'] is False
