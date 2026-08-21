"""Enterprise 17.1 Production Release Candidate Evidence Pack & Go/No-Go Board."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='17.1.0'
CRITICAL=('regression_ci','disaster_recovery','security_hardening')
def _id(*p:Any)->str:return 'GOVRC-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def evaluate_release_candidate(gates:dict[str,Any], approvals:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; required=tuple(rules.get('required_gates',('integration_quality','regression_ci','disaster_recovery','security_hardening','excel_master','power_bi','documentation'))); rows=[]
 for g in required:
  x=gates.get(g,{}) if isinstance(gates.get(g,{}),dict) else {'passed':bool(gates.get(g))}; rows.append({'gate':g,'passed':bool(x.get('passed',False)),'score_pct':float(x.get('score_pct',100 if x.get('passed') else 0) or 0),'evidence_ref':x.get('evidence_ref'),'conditional':bool(x.get('conditional',False))})
 blockers=[r['gate'] for r in rows if not r['passed'] and r['gate'] in CRITICAL]; noncritical=[r['gate'] for r in rows if not r['passed'] and r['gate'] not in CRITICAL]; evidence_complete=all(r['evidence_ref'] for r in rows if r['passed']); release_owner=bool(approvals.get('release_owner_approved',False)); security_owner=bool(approvals.get('security_owner_approved',False)); board=bool(approvals.get('board_go_no_go_confirmed',False))
 if blockers: decision='NO-GO'
 elif noncritical or not evidence_complete: decision='CONDITIONAL GO'
 elif release_owner and security_owner and board: decision='GO'
 else: decision='CONDITIONAL GO'
 return {'production_release_candidate_go_no_go_version':ENGINE_VERSION,'release_candidate_id':_id(decision,len(blockers),len(noncritical)),'decision':decision,'gate_matrix':rows,'critical_blockers':blockers,'noncritical_open_items':noncritical,'evidence_complete':evidence_complete,'release_owner_approved':release_owner,'security_owner_approved':security_owner,'board_go_no_go_confirmed':board,'production_release_authorized':decision=='GO','manual_release_execution_required':decision=='GO','automatic_production_release':False,'automatic_conditional_waiver':False,'next_action':'Voer de handmatige productie-release uit volgens het goedgekeurde releaseplan.' if decision=='GO' else ('Sluit openstaande niet-kritieke punten en completeer bewijs/goedkeuringen.' if decision=='CONDITIONAL GO' else 'Herstel alle kritieke blockers en voer de volledige release candidate gate opnieuw uit.')}
