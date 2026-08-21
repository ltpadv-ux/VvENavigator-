from src.automated_regression_matrix_ci_evidence_gate import evaluate_regression_matrix,DEFAULT_FLOWS

def _ok(): return {f:{'passed':True,'tests':3,'failures':0,'evidence_ref':f'ev-{f}'} for f in DEFAULT_FLOWS}
def test_full_matrix_and_green_ci_pass():
 x=evaluate_regression_matrix(_ok(),{'green':True,'run_id':123,'commit_sha':'abc'}); assert x['production_evidence_ready'] is True and x['regression_coverage_pct']==100
def test_failed_flow_blocks_gate():
 r=_ok(); r['execution_to_audit']['passed']=False; x=evaluate_regression_matrix(r,{'green':True,'run_id':123,'commit_sha':'abc'}); assert x['production_evidence_ready'] is False and 'REGRESSION_FAIL:execution_to_audit' in x['blockers']
def test_missing_ci_evidence_blocks_gate():
 x=evaluate_regression_matrix(_ok(),{'green':True}); assert x['evidence_complete'] is False and x['automatic_release'] is False
