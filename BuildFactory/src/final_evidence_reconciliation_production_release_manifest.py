"""Enterprise 17.7 Final Evidence Reconciliation & Production Release Manifest."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='17.7.0'
REQUIRED=('ci','regression','security','disaster_recovery','excel','power_bi','documentation','rc1_evidence')
CRITICAL=('ci','regression','security','disaster_recovery')
def _id(*parts:Any)->str:
    raw='|'.join(str(x) for x in parts)
    return 'GOVREL-'+sha256(raw.encode()).hexdigest()[:12].upper()
def reconcile_release_evidence(evidence:dict[str,Any], approvals:dict[str,Any], release:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
    rules=rules or {}; required=tuple(rules.get('required_evidence',REQUIRED)); critical=set(rules.get('critical_evidence',CRITICAL)); rows=[]
    for name in required:
        raw=evidence.get(name,{}) if isinstance(evidence.get(name,{}),dict) else {'passed':bool(evidence.get(name))}
        passed=bool(raw.get('passed',raw.get('closed',False))); ref=raw.get('evidence_ref'); verified=bool(raw.get('verified',passed)); commit=raw.get('commit_sha'); run_id=raw.get('run_id')
        rows.append({'evidence':name,'passed':passed,'verified':verified,'evidence_ref':ref,'commit_sha':commit,'run_id':run_id,'critical':name in critical,'closed':passed and verified and bool(ref)})
    closed=sum(1 for r in rows if r['closed']); closure_pct=round(100*closed/len(rows),1) if rows else 0.0
    critical_blockers=[r['evidence'] for r in rows if r['critical'] and not r['closed']]; open_items=[r['evidence'] for r in rows if not r['closed']]
    security_ok=bool(approvals.get('security_owner_approved',False)); release_ok=bool(approvals.get('release_owner_approved',False)); board_ok=bool(approvals.get('board_go_no_go_confirmed',False)); approvals_ok=security_ok and release_ok and board_ok
    version=str(release.get('version') or ''); target_commit=str(release.get('commit_sha') or ''); tag=str(release.get('tag') or '')
    identity_ok=bool(version and target_commit and tag)
    min_closure=float(rules.get('minimum_closure_pct',100)); manifest_complete=closure_pct>=min_closure and not open_items and approvals_ok and identity_ok
    if critical_blockers: decision='NO-GO'
    elif not manifest_complete: decision='HOLD'
    else: decision='GO'
    manifest_id=_id(version,target_commit,tag,decision,closure_pct)
    manifest={
        'manifest_id':manifest_id,'version':version,'target_commit_sha':target_commit,'release_tag':tag,'decision':decision,
        'evidence_closure_pct':closure_pct,'evidence_refs':{r['evidence']:r['evidence_ref'] for r in rows if r['closed']},
        'approvals':{'security_owner':security_ok,'release_owner':release_ok,'go_no_go_board':board_ok},
        'critical_blockers':critical_blockers,'open_items':open_items
    }
    return {
        'final_evidence_reconciliation_production_release_manifest_version':ENGINE_VERSION,
        'release_manifest_id':manifest_id,'decision':decision,'release_manifest':manifest,'evidence_matrix':rows,
        'evidence_closure_pct':closure_pct,'critical_blockers':critical_blockers,'open_items':open_items,
        'all_required_approvals':approvals_ok,'release_identity_complete':identity_ok,'manifest_complete':manifest_complete,
        'production_release_authorized':decision=='GO','manual_release_tag_required':decision=='GO','manual_production_release_required':decision=='GO',
        'immutable_evidence_archive_required':decision=='GO','automatic_release':False,'automatic_tagging':False,'automatic_evidence_waiver':False,
        'next_action':'Maak handmatig de release-tag, voer productie-release uit en archiveer het immutable evidence manifest.' if decision=='GO' else ('Sluit ontbrekend bewijs, release-identiteit en/of goedkeuringen.' if decision=='HOLD' else 'Herstel kritieke releaseblockers en voer de volledige reconciliatie opnieuw uit.')
    }
