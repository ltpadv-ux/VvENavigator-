from src.governance_policy_drift_detection import analyze_policy_drift

def test_consistent_history():
 x=analyze_policy_drift([{'divergence_score':10},{'divergence_score':15},{'divergence_score':12}]); assert x['status']=='BELEID CONSISTENT'; assert x['policy_drift_detected'] is False

def test_conscious_policy_evolution():
 h=[{'divergence_score':50,'material_divergence':True,'board_rationale_complete':True},{'divergence_score':55,'material_divergence':True,'board_rationale_complete':True},{'divergence_score':60,'material_divergence':True,'board_rationale_complete':True}]
 x=analyze_policy_drift(h); assert x['status']=='BEWUSTE BELEIDSONTWIKKELING'; assert x['conscious_policy_evolution'] is True

def test_unexplained_drift_alerts_red():
 h=[{'divergence_score':50,'material_divergence':True,'board_rationale_complete':False},{'divergence_score':55,'material_divergence':True,'board_rationale_complete':True},{'divergence_score':60,'material_divergence':True,'board_rationale_complete':True}]
 x=analyze_policy_drift(h); assert x['status']=='POLICY DRIFT - REVIEW VEREIST'; assert any(a['severity']=='ROOD' for a in x['alerts'])
