from src.final_production_validation_rc1 import evaluate_rc1, REQUIRED

def _ok(): return {k:{'passed':True,'score_pct':100,'evidence_ref':f'ev-{k}'} for k in REQUIRED}
def test_full_evidence_is_rc1_ready():
 x=evaluate_rc1(_ok()); assert x['release_candidate_rc1_ready'] is True and x['status']=='RC1 VALIDATED'
def test_failed_check_blocks_rc1():
 c=_ok(); c['power_bi']['passed']=False; x=evaluate_rc1(c); assert x['release_candidate_rc1_ready'] is False and 'power_bi' in x['blockers']
def test_missing_evidence_blocks_rc1():
 c=_ok(); c['ci']['evidence_ref']=None; x=evaluate_rc1(c); assert x['evidence_complete'] is False and x['automatic_release'] is False
