"""Enterprise 16.7 End-to-End Integration Quality Gate & Production Readiness Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='16.7.0'
def _id(*p:Any)->str:return 'GOVPRD-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def evaluate_production_readiness(signals:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; required=list(rules.get('required_domains') or ['finance','mjop','risk','governance','audit','digital_twin','scenario','model_controls','excel_master','ci'])
 weights=rules.get('weights') or {k:1 for k in required}; rows=[]; blockers=[]; weighted=0.0; total_w=0.0
 for domain in required:
  raw=signals.get(domain,{}); passed=bool(raw.get('passed',False)); score=float(raw.get('score_pct',100 if passed else 0) or 0); score=max(0,min(100,score)); w=float(weights.get(domain,1) or 1); total_w+=w; weighted+=score*w
  critical=bool(raw.get('critical',domain in {'finance','mjop','governance','audit','ci'})); rows.append({'domain':domain,'passed':passed,'score_pct':round(score,1),'critical':critical,'evidence':raw.get('evidence')})
  if critical and not passed:blockers.append(f'Kritieke productiedomein niet geslaagd: {domain}.')
 readiness=round(weighted/total_w,1) if total_w else 0.0; min_readiness=float(rules.get('minimum_production_readiness_pct',95)); ci_required=bool(rules.get('require_ci_green',True)); ci_green=bool((signals.get('ci') or {}).get('passed',False));
 if ci_required and not ci_green and 'Kritieke productiedomein niet geslaagd: ci.' not in blockers:blockers.append('CI is niet bewezen groen.')
 production_ready=(not blockers and readiness>=min_readiness)
 status='PRODUCTION READY' if production_ready else ('RELEASE CANDIDATE - HARDENING VEREIST' if readiness>=90 else 'INTEGRATIE NIET PRODUCTIEGEREED')
 return {'end_to_end_integration_quality_gate_version':ENGINE_VERSION,'readiness_id':_id(readiness,len(blockers),len(required)),'status':status,'production_readiness_pct':readiness,'minimum_production_readiness_pct':min_readiness,'domain_results':rows,'blockers':blockers,'production_ready':production_ready,'requires_full_regression_suite':True,'requires_ci_green':ci_required,'requires_backup_restore_test':True,'requires_security_review':True,'requires_release_notes':True,'human_release_approval_required':True,'automatic_production_release':False,'next_action':'Voer volledige regression, CI, backup/restore en release-review uit vóór productie-release.' if not production_ready else 'Laat release owner de productie-release expliciet goedkeuren.'}
