from src.autonomous_governance_learning_loop import build_learning_proposal

def test_repeated_cost_variance_creates_proposal():
 h=[{'price_variance_pct':8},{'price_variance_pct':7},{'price_variance_pct':9}]; x=build_learning_proposal(h,{}); assert x['proposal_count']==1 and x['requires_backtest'] is True
def test_step_is_bounded():
 h=[{'mjop_variance_pct':30}]*3; x=build_learning_proposal(h,{}, {'max_parameter_step_pct':10}); assert x['parameter_proposals'][0]['proposed_delta_pct']==10
def test_no_automatic_model_update():
 x=build_learning_proposal([],{}); assert x['automatic_model_update'] is False and x['automatic_risk_appetite_change'] is False
