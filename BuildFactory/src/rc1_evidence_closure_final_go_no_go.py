"""Enterprise 17.3 RC1 Evidence Closure & Final Go/No-Go Execution."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='17.3.0'
CRITICAL=('ci','regression','security','disaster_recovery')
def _id(*p:Any)->str:return 'GOVFIN-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def close_rc1_and_decide(checks:dict[str,Any], approvals:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; required=tuple(rules.get('required_checks',('ci','regression','security','disaster_recovery','excel','power_bi','documentation','rc1_evidence'))); rows=[]
 for name in required:
  raw=checks.get(name,{}) if isinstance(checks.get(name,{}),dict) else {'passed':bool(checks.get(name))}; passed=bool(raw.get('passed',False)); ev=raw.get('evidence_ref'); rows.append({'check':name,'passed':passed,'evidence_ref':ev,'closed':passed and bool(ev),'critical':name in CRITICAL})
 critical_blockers=[r['check'] for r in rows if r['critical'] and not r['closed']]; open_items=[r['check'] for r in rows if not r['closed']]; closure_pct=round(100*sum(r['closed'] for r in rows)/len(rows),1) if rows else 0.0
 min_pct=float(rules.get('minimum_evidence_closure_pct',100)); approvals_ok=all(bool(approvals.get(k,False)) for k in ('security_owner_approved','release_owner_approved','board_go_no_go_confirmed')); evidence_closed=closure_pct>=min_pct and not open_items
 if critical_blockers: decision='NO-GO'
 elif not evidence_closed or not approvals_ok: decision='HOLD'
 else: decision='GO'
 return {'rc1_evidence_closure_final_go_no_go_version':ENGINE_VERSION,'final_decision_id':_id(decision,closure_pct,len(open_items)),'decision':decision,'evidence_closure_pct':closure_pct,'evidence_matrix':rows,'critical_blockers':critical_blockers,'open_items':open_items,'all_required_approvals':approvals_ok,'rc1_evidence_closed':evidence_closed,'production_release_authorized':decision=='GO','manual_release_required':decision=='GO','release_tag_allowed':decision=='GO','automatic_release':False,'automatic_evidence_waiver':False,'next_action':'Maak handmatig de goedgekeurde production release/tag en archiveer het evidence pack.' if decision=='GO' else ('Sluit ontbrekend bewijs en/of goedkeuringen vóór een nieuwe finale beslissing.' if decision=='HOLD' else 'Herstel kritieke blockers en voer RC1-validatie en Go/No-Go opnieuw uit.')}
