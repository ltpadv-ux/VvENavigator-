"""Enterprise 18.1 GA Evidence Closure & Release Tag Readiness."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='18.1.0'
REQUIRED=('ci','regression','security','disaster_recovery','excel','power_bi','documentation','rc1_evidence','authorization_pack')
CRITICAL=('ci','regression','security','disaster_recovery','authorization_pack')
def _id(*p:Any)->str:return 'GOVTAG-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:12].upper()
def evaluate_ga_tag_readiness(evidence:dict[str,Any], release:dict[str,Any], approvals:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; required=tuple(rules.get('required_evidence',REQUIRED)); critical=set(rules.get('critical_evidence',CRITICAL)); target=str(release.get('commit_sha') or ''); version=str(release.get('version') or ''); tag=str(release.get('tag') or ''); rows=[]
 for name in required:
  raw=evidence.get(name,{}) if isinstance(evidence.get(name,{}),dict) else {'passed':bool(evidence.get(name))}; passed=bool(raw.get('passed',raw.get('closed',False))); verified=bool(raw.get('verified',passed)); ref=raw.get('evidence_ref'); sha=str(raw.get('commit_sha') or ''); aligned=(not sha) or (bool(target) and sha==target); rows.append({'evidence':name,'closed':passed and verified and bool(ref) and aligned,'critical':name in critical,'evidence_ref':ref,'commit_aligned':aligned})
 open_items=[r['evidence'] for r in rows if not r['closed']]; critical_blockers=[r['evidence'] for r in rows if r['critical'] and not r['closed']]; closure=round(100*sum(r['closed'] for r in rows)/len(rows),1) if rows else 0.0
 identity_ok=bool(version and target and tag) and tag==f'v{version}'; approvals_ok=all(bool(approvals.get(k,False)) for k in ('security_owner_approved','release_owner_approved','board_go_no_go_confirmed','ga_promotion_approved')); tag_ready=closure>=float(rules.get('minimum_closure_pct',100)) and not open_items and identity_ok and approvals_ok
 decision='NO-GO' if critical_blockers else ('TAG-READY' if tag_ready else 'HOLD')
 return {'ga_evidence_closure_release_tag_readiness_version':ENGINE_VERSION,'tag_readiness_id':_id(version,target,tag,decision),'decision':decision,'evidence_closure_pct':closure,'evidence_matrix':rows,'critical_blockers':critical_blockers,'open_items':open_items,'release_identity_valid':identity_ok,'approvals_complete':approvals_ok,'ga_tag_ready':decision=='TAG-READY','manual_tag_creation_required':decision=='TAG-READY','automatic_tag_creation':False,'automatic_release':False,'next_action':'Maak handmatig de GA-tag op exact de gevalideerde commit en voer daarna de GA-release uit.' if decision=='TAG-READY' else ('Sluit resterend bewijs/goedkeuringen of corrigeer release-identiteit.' if decision=='HOLD' else 'Herstel kritieke blockers en herhaal de GA evidence closure.')}
