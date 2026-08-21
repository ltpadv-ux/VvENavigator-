from src.production_ga_release_gate import evaluate_ga_release

def _e(sha='abc'):
    keys=('ci','regression','security','disaster_recovery','excel','power_bi','documentation','rc1_evidence','authorization_pack')
    return {k:{'passed':True,'verified':True,'evidence_ref':'ev-'+k,'commit_sha':sha if k in ('ci','regression','authorization_pack') else None} for k in keys}
def _r(): return {'version':'18.0.0','commit_sha':'abc','tag':'v18.0.0','channel':'GA'}
def _a(): return {'security_owner_approved':True,'release_owner_approved':True,'board_go_no_go_confirmed':True,'ga_promotion_approved':True}
def test_full_evidence_is_ga_ready():
    x=evaluate_ga_release(_e(),_r(),_a()); assert x['decision']=='GA-READY' and x['ga_release_ready'] is True and x['automatic_release'] is False
def test_critical_authorization_pack_failure_is_no_go():
    e=_e(); e['authorization_pack']['passed']=False; x=evaluate_ga_release(e,_r(),_a()); assert x['decision']=='NO-GO' and 'authorization_pack' in x['critical_blockers']
def test_missing_noncritical_evidence_holds():
    e=_e(); e['power_bi']['evidence_ref']=None; x=evaluate_ga_release(e,_r(),_a()); assert x['decision']=='HOLD'
