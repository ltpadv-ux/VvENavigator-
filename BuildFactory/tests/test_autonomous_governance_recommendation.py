from src.autonomous_governance_recommendation import build_governance_recommendations

def test_no_signal_no_action():
 x=build_governance_recommendations({}); assert x['status']=='GEEN DIRECTE ACTIE'; assert x['automatic_decision'] is False

def test_red_treasury_is_critical():
 x=build_governance_recommendations({'portfolio_treasury_control_tower':{'status':'ROOD','treasury_score':30}}); assert x['recommendations'][0]['priority']=='KRITIEK'; assert x['recommendations'][0]['topic']=='liquidity'

def test_red_variance_uses_corrective_cost():
 r={'strategic_mandate_variance_control':{'status':'ROOD'},'predictive_corrective_action_optimizer':{'ranking':[{'estimated_corrective_cost':12500}]}}
 x=build_governance_recommendations(r); assert x['recommendations'][0]['financial_impact']==12500; assert x['human_decision_required'] is True
