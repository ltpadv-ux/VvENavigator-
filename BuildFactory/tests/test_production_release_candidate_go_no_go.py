from src.production_release_candidate_go_no_go import evaluate_release_candidate

def _g(p=True): return {'passed':p,'score_pct':100 if p else 0,'evidence_ref':'ev' if p else None}
def test_all_gates_and_approvals_give_go():
 gates={k:_g() for k in ('integration_quality','regression_ci','disaster_recovery','security_hardening','excel_master','power_bi','documentation')}; x=evaluate_release_candidate(gates,{'release_owner_approved':True,'security_owner_approved':True,'board_go_no_go_confirmed':True}); assert x['decision']=='GO' and x['production_release_authorized'] is True
def test_critical_failure_is_no_go():
 gates={k:_g() for k in ('integration_quality','regression_ci','disaster_recovery','security_hardening','excel_master','power_bi','documentation')}; gates['security_hardening']=_g(False); x=evaluate_release_candidate(gates,{}); assert x['decision']=='NO-GO'
def test_noncritical_gap_is_conditional():
 gates={k:_g() for k in ('integration_quality','regression_ci','disaster_recovery','security_hardening','excel_master','power_bi','documentation')}; gates['power_bi']=_g(False); x=evaluate_release_candidate(gates,{}); assert x['decision']=='CONDITIONAL GO' and x['automatic_production_release'] is False
