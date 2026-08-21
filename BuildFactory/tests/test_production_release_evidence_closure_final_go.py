from src.production_release_evidence_closure_final_go import execute_final_go

def _e(commit='abc'):
    return {k:{'passed':True,'verified':True,'evidence_ref':'ev-'+k,'commit_sha':commit if k in ('ci','regression') else None} for k in ('ci','regression','security','disaster_recovery','excel','power_bi','documentation','rc1_evidence')}
def _a(): return {'security_owner_approved':True,'release_owner_approved':True,'board_go_no_go_confirmed':True}
def test_full_closure_gives_go():
    x=execute_final_go(_e(),_a(),{'version':'17.8.0','commit_sha':'abc','tag':'v17.8.0'}); assert x['decision']=='GO' and x['production_release_authorized'] is True
def test_commit_mismatch_blocks():
    e=_e('wrong'); x=execute_final_go(e,_a(),{'version':'17.8.0','commit_sha':'abc','tag':'v17.8.0'}); assert x['decision']=='NO-GO' and 'ci' in x['critical_blockers']
def test_missing_approval_holds_and_never_auto_releases():
    x=execute_final_go(_e(),{}, {'version':'17.8.0','commit_sha':'abc','tag':'v17.8.0'}); assert x['decision']=='HOLD' and x['automatic_release'] is False
