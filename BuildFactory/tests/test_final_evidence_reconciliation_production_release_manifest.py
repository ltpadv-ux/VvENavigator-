from src.final_evidence_reconciliation_production_release_manifest import reconcile_release_evidence, REQUIRED

def _evidence():
    return {k:{'passed':True,'verified':True,'evidence_ref':'ev-'+k} for k in REQUIRED}
def _approvals():
    return {'security_owner_approved':True,'release_owner_approved':True,'board_go_no_go_confirmed':True}
def _release():
    return {'version':'17.7.0','commit_sha':'abc123','tag':'v17.7.0'}
def test_complete_manifest_gives_go():
    x=reconcile_release_evidence(_evidence(),_approvals(),_release()); assert x['decision']=='GO' and x['manifest_complete'] is True and x['production_release_authorized'] is True
def test_missing_noncritical_evidence_holds():
    e=_evidence(); e['power_bi']['evidence_ref']=None; x=reconcile_release_evidence(e,_approvals(),_release()); assert x['decision']=='HOLD' and 'power_bi' in x['open_items']
def test_missing_critical_evidence_is_no_go_and_never_auto_release():
    e=_evidence(); e['ci']['passed']=False; x=reconcile_release_evidence(e,_approvals(),_release()); assert x['decision']=='NO-GO' and x['automatic_release'] is False and 'ci' in x['critical_blockers']
def test_release_identity_is_required():
    x=reconcile_release_evidence(_evidence(),_approvals(),{}); assert x['decision']=='HOLD' and x['release_identity_complete'] is False
