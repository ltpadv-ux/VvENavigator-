from src.ci_run_result_closure_rc1_ingestion import ingest_ci_run_result

def test_green_run_closes_and_builds_rc1_patch():
 run={'id':123,'head_sha':'abc','status':'completed','conclusion':'success','name':'Enterprise CI'}; jobs=[{'id':1,'name':'test','status':'completed','conclusion':'success'}]; artifacts=[{'name':'vve-navigator-production-verification'}]; x=ingest_ci_run_result(run,jobs,artifacts); assert x['ci_run_closed'] is True and x['ready_for_rc1_ingestion'] is True and x['rc1_evidence_patch']['ci']['verified'] is True
def test_missing_artifact_holds():
 run={'id':123,'head_sha':'abc','status':'completed','conclusion':'success','name':'Enterprise CI'}; jobs=[{'id':1,'name':'test','status':'completed','conclusion':'success'}]; x=ingest_ci_run_result(run,jobs,[]); assert x['ci_run_closed'] is False and 'ARTIFACT_MISSING:vve-navigator-production-verification' in x['blockers']
def test_failed_job_never_auto_releases():
 run={'id':123,'head_sha':'abc','status':'completed','conclusion':'failure','name':'Enterprise CI'}; jobs=[{'id':1,'name':'test','status':'completed','conclusion':'failure'}]; x=ingest_ci_run_result(run,jobs,[]); assert x['decision']=='HOLD' and x['automatic_release'] is False and x['automatic_go_no_go'] is False
