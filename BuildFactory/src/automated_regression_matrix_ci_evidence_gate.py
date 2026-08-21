"""Enterprise 16.8 Automated Regression Matrix & CI Evidence Gate."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='16.8.0'
DEFAULT_FLOWS=('finance_to_mjop','mjop_to_risk','risk_to_scenario','scenario_to_alv','alv_to_activation','activation_to_execution','execution_to_audit','audit_to_close','close_to_digital_twin','digital_twin_to_learning')
def _id(*p:Any)->str:return 'GOVREG-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def evaluate_regression_matrix(results:dict[str,Any], ci:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; required=tuple(rules.get('required_flows',DEFAULT_FLOWS)); rows=[]
 for flow in required:
  r=results.get(flow,{}) if isinstance(results.get(flow,{}),dict) else {'passed':bool(results.get(flow))}
  passed=bool(r.get('passed',False)); rows.append({'flow':flow,'passed':passed,'tests':int(r.get('tests',0) or 0),'failures':int(r.get('failures',0) or 0),'evidence_ref':r.get('evidence_ref')})
 passed_count=sum(1 for r in rows if r['passed']); coverage=round(100*passed_count/len(rows),1) if rows else 0.0
 ci_green=bool(ci.get('green',False)); ci_run_id=ci.get('run_id'); ci_commit=ci.get('commit_sha'); evidence_complete=all(r['evidence_ref'] for r in rows if r['passed']) and bool(ci_run_id) and bool(ci_commit)
 blockers=[]
 blockers += [f"REGRESSION_FAIL:{r['flow']}" for r in rows if not r['passed']]
 if not ci_green:blockers.append('CI_NOT_GREEN')
 if not evidence_complete:blockers.append('CI_EVIDENCE_INCOMPLETE')
 min_cov=float(rules.get('minimum_regression_coverage_pct',100));
 if coverage<min_cov:blockers.append('REGRESSION_COVERAGE_BELOW_GATE')
 ready=not blockers
 return {'automated_regression_matrix_ci_evidence_gate_version':ENGINE_VERSION,'evidence_gate_id':_id(ci_commit,coverage,len(blockers)),'status':'CI EVIDENCE GATE PASSED' if ready else 'CI EVIDENCE GATE BLOCKED','required_flows':list(required),'regression_matrix':rows,'passed_flows':passed_count,'total_flows':len(rows),'regression_coverage_pct':coverage,'ci_green':ci_green,'ci_run_id':ci_run_id,'ci_commit_sha':ci_commit,'evidence_complete':evidence_complete,'blockers':blockers,'production_evidence_ready':ready,'requires_human_release_approval':ready,'automatic_release':False,'automatic_gate_override':False,'next_action':'Laat release owner het evidence pack beoordelen en expliciet vrijgeven.' if ready else 'Herstel regressies/CI, voeg ontbrekend bewijs toe en voer de volledige matrix opnieuw uit.'}
