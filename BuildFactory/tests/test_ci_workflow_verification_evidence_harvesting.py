from src.ci_workflow_verification_evidence_harvesting import verify_ci_evidence, REQUIRED_WORKFLOW_CONTROLS

def _workflow(): return {'name':'Enterprise CI','path':'.github/workflows/enterprise-ci.yml','controls':{k:True for k in REQUIRED_WORKFLOW_CONTROLS}}
def test_green_ci_with_evidence_passes():
 x=verify_ci_evidence(_workflow(),{'run_id':123,'commit_sha':'abc','conclusion':'success','junit_evidence_ref':'junit.xml','artifact_evidence_ref':'artifact:verification'}); assert x['ready_for_rc1_evidence_pack'] is True
def test_missing_junit_blocks():
 x=verify_ci_evidence(_workflow(),{'run_id':123,'commit_sha':'abc','conclusion':'success','artifact_evidence_ref':'artifact'}); assert 'JUNIT_EVIDENCE_MISSING' in x['blockers']
def test_missing_control_and_failed_run_block():
 w=_workflow(); w['controls']['pytest']=False; x=verify_ci_evidence(w,{'run_id':1,'commit_sha':'x','conclusion':'failure','junit_evidence_ref':'j','artifact_evidence_ref':'a'}); assert x['ci_green'] is False and 'WORKFLOW_CONTROLS_MISSING' in x['blockers'] and x['automatic_release'] is False
