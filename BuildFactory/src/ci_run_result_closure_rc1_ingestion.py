"""Enterprise 17.6 CI Run Result Closure & RC1 Evidence Ingestion."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='17.6.0'
REQUIRED_ARTIFACTS=('vve-navigator-production-verification',)
def _id(*p:Any)->str:return 'GOVCIR-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def ingest_ci_run_result(run:dict[str,Any], jobs:list[dict[str,Any]]|None=None, artifacts:list[dict[str,Any]]|None=None, rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; jobs=jobs or []; artifacts=artifacts or []
 run_id=run.get('id') or run.get('run_id'); sha=run.get('head_sha') or run.get('commit_sha'); status=str(run.get('status','')).lower(); conclusion=str(run.get('conclusion','')).lower(); workflow=run.get('name') or run.get('workflow_name')
 required_workflow=rules.get('workflow_name','Enterprise CI'); required_artifacts=tuple(rules.get('required_artifacts',REQUIRED_ARTIFACTS))
 completed=status=='completed'; green=conclusion=='success'; workflow_match=workflow==required_workflow
 job_rows=[]
 for j in jobs:
  jc=str(j.get('conclusion','')).lower(); js=str(j.get('status','')).lower(); job_rows.append({'job_id':j.get('id'),'name':j.get('name'),'status':js,'conclusion':jc,'passed':js=='completed' and jc=='success'})
 all_jobs_green=bool(job_rows) and all(j['passed'] for j in job_rows)
 artifact_names={a.get('name') for a in artifacts}; missing_artifacts=[a for a in required_artifacts if a not in artifact_names]
 evidence={'run_id':run_id,'commit_sha':sha,'workflow':workflow,'status':status,'conclusion':conclusion,'jobs':job_rows,'artifact_names':sorted(x for x in artifact_names if x)}
 blockers=[]
 if not workflow_match:blockers.append('WORKFLOW_MISMATCH')
 if not completed:blockers.append('RUN_NOT_COMPLETED')
 if not green:blockers.append('RUN_NOT_GREEN')
 if not run_id:blockers.append('RUN_ID_MISSING')
 if not sha:blockers.append('COMMIT_SHA_MISSING')
 if not all_jobs_green:blockers.append('JOBS_NOT_ALL_GREEN')
 blockers.extend(f'ARTIFACT_MISSING:{a}' for a in missing_artifacts)
 closed=not blockers
 ci_evidence_ref=f'github-actions-run:{run_id}@{sha}' if closed else None
 rc1_patch={'ci':{'present':closed,'verified':closed,'evidence_ref':ci_evidence_ref},'regression':{'present':closed,'verified':closed,'evidence_ref':f'junit:{run_id}' if closed else None}}
 decision='GO_EVIDENCE_READY' if closed else ('HOLD' if completed else 'WAITING_FOR_RUN_COMPLETION')
 return {'ci_run_result_closure_rc1_ingestion_version':ENGINE_VERSION,'ci_run_closure_id':_id(run_id,sha,decision),'decision':decision,'ci_run_closed':closed,'ci_green':green,'workflow_match':workflow_match,'all_jobs_green':all_jobs_green,'missing_artifacts':missing_artifacts,'blockers':blockers,'evidence':evidence,'ci_evidence_ref':ci_evidence_ref,'rc1_evidence_patch':rc1_patch,'ready_for_rc1_ingestion':closed,'human_evidence_review_required':closed,'automatic_release':False,'automatic_go_no_go':False,'next_action':'Laat evidence owner de CI-run verifiëren en voeg de patch toe aan het RC1 Closure Pack.' if closed else 'Wacht op een voltooide groene Enterprise CI-run of herstel de genoemde blockers.'}
