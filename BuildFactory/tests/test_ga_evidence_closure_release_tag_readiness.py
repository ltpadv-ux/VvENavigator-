from src.ga_evidence_closure_release_tag_readiness import evaluate_ga_tag_readiness

def _e(sha='abc'): return {k:{'passed':True,'verified':True,'evidence_ref':'ev-'+k,'commit_sha':sha if k in ('ci','regression','authorization_pack') else None} for k in ('ci','regression','security','disaster_recovery','excel','power_bi','documentation','rc1_evidence','authorization_pack')}
def _a(): return {'security_owner_approved':True,'release_owner_approved':True,'board_go_no_go_confirmed':True,'ga_promotion_approved':True}
def test_complete_ga_evidence_is_tag_ready():
 x=evaluate_ga_tag_readiness(_e(),{'version':'18.1.0','commit_sha':'abc','tag':'v18.1.0'},_a()); assert x['decision']=='TAG-READY' and x['ga_tag_ready'] is True
def test_wrong_tag_holds():
 x=evaluate_ga_tag_readiness(_e(),{'version':'18.1.0','commit_sha':'abc','tag':'latest'},_a()); assert x['decision']=='HOLD' and x['release_identity_valid'] is False
def test_critical_authorization_pack_mismatch_is_no_go():
 e=_e(); e['authorization_pack']['commit_sha']='old'; x=evaluate_ga_tag_readiness(e,{'version':'18.1.0','commit_sha':'abc','tag':'v18.1.0'},_a()); assert x['decision']=='NO-GO' and 'authorization_pack' in x['critical_blockers']
