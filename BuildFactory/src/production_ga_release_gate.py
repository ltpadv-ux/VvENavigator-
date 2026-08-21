"""Enterprise 18.0 Production GA Release Gate."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='18.0.0'
REQUIRED=('ci','regression','security','disaster_recovery','excel','power_bi','documentation','rc1_evidence','authorization_pack')
CRITICAL=('ci','regression','security','disaster_recovery','authorization_pack')
def _id(*p:Any)->str:return 'GOVGA-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:12].upper()
def evaluate_ga_release(evidence:dict[str,Any], release:dict[str,Any], approvals:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; required=tuple(rules.get('required_evidence',REQUIRED)); critical=set(rules.get('critical_evidence',CRITICAL)); target=str(release.get('commit_sha') or ''); version=str(release.get('version') or ''); tag=str(release.get('tag') or ''); channel=str(release.get('channel') or 'GA'); rows=[]
 for name in required:
  raw=evidence.get(name,{}) if isinstance(evidence.get(name,{}),dict) else {'passed':bool(evidence.get(name))}; passed=bool(raw.get('passed',raw.get('closed',False))); verified=bool(raw.get('verified',passed)); ref=raw.get('evidence_ref'); sha=str(raw.get('commit_sha') or ''); aligned=(not sha) or (bool(target) and sha==target); rows.append({'evidence':name,'passed':passed,'verified':verified,'evidence_ref':ref,'commit_sha':sha or None,'commit_aligned':aligned,'critical':name in critical,'closed':passed and verified and bool(ref) and aligned})
 open_items=[r['evidence'] for r in rows if not r['closed']]; blockers=[r['evidence'] for r in rows if r['critical'] and not r['closed']]; closure=round(100*sum(r['closed'] for r in rows)/len(rows),1) if rows else 0.0
 identity_ok=bool(version and target and tag and channel=='GA'); approvals_ok=all(bool(approvals.get(k,False)) for k in ('security_owner_approved','release_owner_approved','board_go_no_go_confirmed','ga_promotion_approved'))
 min_closure=float(rules.get('minimum_ga_closure_pct',100)); ready=closure>=min_closure and not open_items and identity_ok and approvals_ok
 decision='NO-GO' if blockers else ('GA-READY' if ready else 'HOLD'); gate_id=_id(version,target,tag,decision,closure)
 return {'production_ga_release_gate_version':ENGINE_VERSION,'ga_gate_id':gate_id,'decision':decision,'ga_release_ready':decision=='GA-READY','evidence_closure_pct':closure,'evidence_matrix':rows,'critical_blockers':blockers,'open_items':open_items,'release_identity_complete':identity_ok,'all_required_approvals':approvals_ok,'manual_ga_tag_required':decision=='GA-READY','manual_production_release_required':decision=='GA-READY','immutable_evidence_archive_required':decision=='GA-READY','automatic_ga_promotion':False,'automatic_release':False,'ga_manifest':{'gate_id':gate_id,'version':version,'commit_sha':target,'tag':tag,'channel':channel,'decision':decision,'evidence_refs':{r['evidence']:r['evidence_ref'] for r in rows if r['closed']}},'next_action':'Promoveer handmatig naar GA, maak de release-tag en archiveer het immutable evidence pack.' if decision=='GA-READY' else ('Sluit resterend bewijs en/of GA-goedkeuringen.' if decision=='HOLD' else 'Herstel kritieke blockers en herhaal de volledige GA-gate.')}
