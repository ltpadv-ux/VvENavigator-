from src.final_production_evidence_completion_release_authorization import authorize_release

def _e(sha='abc'): return {k:{'passed':True,'verified':True,'evidence_ref':'ev-'+k,'commit_sha':sha if k in ('ci','regression') else None} for k in ('ci','regression','security','disaster_recovery','excel','power_bi','documentation','rc1_evidence')}
def _a(): return {'security_owner_approved':True,'release_owner_approved':True,'board_go_no_go_confirmed':True}
def _r(): return {'version':'17.9.0','commit_sha':'abc','tag':'v17.9.0'}
def test_complete_pack_authorizes_manual_release():
 x=authorize_release(_e(),_a(),_r()); assert x['decision']=='GO' and x['production_release_authorized'] is True and x['automatic_release'] is False
def test_commit_mismatch_blocks_critical_ci():
 e=_e(); e['ci']['commit_sha']='old'; x=authorize_release(e,_a(),_r()); assert x['decision']=='NO-GO' and 'ci' in x['critical_blockers']
def test_missing_noncritical_evidence_holds():
 e=_e(); e['power_bi']['evidence_ref']=None; x=authorize_release(e,_a(),_r()); assert x['decision']=='HOLD' and x['evidence_closure_pct']<100
