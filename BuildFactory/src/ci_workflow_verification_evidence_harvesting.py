"""Enterprise 17.5 CI Workflow Verification & Evidence Harvesting."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='17.5.0'
REQUIRED_WORKFLOW_CONTROLS=('checkout','setup_python','install_dependencies','buildfactory_doctor','pytest','production_verification','artifact_upload')
def _id(*p:Any)->str:return 'GOVCIE-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def verify_ci_evidence(workflow:dict[str,Any], run:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; required=tuple(rules.get('required_workflow_controls',REQUIRED_WORKFLOW_CONTROLS)); controls=workflow.get('controls',{}) if isinstance(workflow.get('controls',{}),dict) else {}; rows=[{'control':c,'present':bool(controls.get(c,False))} for c in required]; missing=[r['control'] for r in rows if not r['present']]
 junit=bool(run.get('junit_evidence_ref')); artifact=bool(run.get('artifact_evidence_ref')); run_id=run.get('run_id'); sha=run.get('commit_sha'); conclusion=str(run.get('conclusion','')).lower(); green=conclusion in {'success','passed','green'}; metadata_complete=bool(run_id and sha); evidence_complete=junit and artifact and metadata_complete; blockers=[]
 if missing:blockers.append('WORKFLOW_CONTROLS_MISSING')
 if not green:blockers.append('CI_RUN_NOT_GREEN')
 if not metadata_complete:blockers.append('CI_RUN_METADATA_INCOMPLETE')
 if not junit:blockers.append('JUNIT_EVIDENCE_MISSING')
 if not artifact:blockers.append('CI_ARTIFACT_EVIDENCE_MISSING')
 ready=not blockers
 return {'ci_workflow_verification_evidence_harvesting_version':ENGINE_VERSION,'ci_evidence_id':_id(run_id,sha,len(blockers)),'status':'CI WORKFLOW & EVIDENCE VERIFIED' if ready else 'CI WORKFLOW & EVIDENCE BLOCKED','workflow_name':workflow.get('name'),'workflow_file':workflow.get('path'),'workflow_controls':rows,'missing_workflow_controls':missing,'run_id':run_id,'commit_sha':sha,'conclusion':conclusion or None,'ci_green':green,'junit_evidence_ref':run.get('junit_evidence_ref'),'artifact_evidence_ref':run.get('artifact_evidence_ref'),'metadata_complete':metadata_complete,'evidence_complete':evidence_complete,'blockers':blockers,'ready_for_rc1_evidence_pack':ready,'human_evidence_review_required':ready,'automatic_release':False,'automatic_evidence_override':False,'next_action':'Voeg dit CI evidence record toe aan het RC1 closure pack en laat evidence owner reviewen.' if ready else 'Herstel workflow/run-bewijs, voer Enterprise CI opnieuw uit en harvest de nieuwe run.'}
