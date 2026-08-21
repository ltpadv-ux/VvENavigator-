from src.rc1_evidence_closure_final_go_no_go import close_rc1_and_decide

def _checks(): return {k:{'passed':True,'evidence_ref':'ev-'+k} for k in ('ci','regression','security','disaster_recovery','excel','power_bi','documentation','rc1_evidence')}
def _approvals(): return {'security_owner_approved':True,'release_owner_approved':True,'board_go_no_go_confirmed':True}
def test_complete_evidence_and_approvals_give_go():
 x=close_rc1_and_decide(_checks(),_approvals()); assert x['decision']=='GO' and x['evidence_closure_pct']==100 and x['production_release_authorized'] is True
def test_missing_noncritical_evidence_holds():
 c=_checks(); c['power_bi']['evidence_ref']=None; x=close_rc1_and_decide(c,_approvals()); assert x['decision']=='HOLD' and 'power_bi' in x['open_items']
def test_critical_failure_is_no_go_and_never_auto_release():
 c=_checks(); c['security']['passed']=False; x=close_rc1_and_decide(c,_approvals()); assert x['decision']=='NO-GO' and x['automatic_release'] is False
