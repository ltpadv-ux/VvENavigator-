from src.production_evidence_runner_rc1_closure_pack import build_evidence_pack, REQUIRED

def _full(): return {k:{'present':True,'verified':True,'evidence_ref':'ev-'+k} for k in REQUIRED}
def test_full_pack_closes():
 x=build_evidence_pack(_full()); assert x['rc1_evidence_pack_closed'] is True and x['closure_pct']==100
def test_missing_critical_blocks():
 e=_full(); e['ci']={'present':False}; x=build_evidence_pack(e); assert x['status']=='RC1 EVIDENCE PACK BLOCKED' and 'ci' in x['critical_missing_evidence']
def test_no_automatic_approval_or_release():
 x=build_evidence_pack({}); assert x['automatic_evidence_approval'] is False and x['automatic_release'] is False
