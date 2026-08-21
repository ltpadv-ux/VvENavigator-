"""Enterprise 17.8 Production Release Evidence Closure & Final GO Execution."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='17.8.0'
REQUIRED=('ci','regression','security','disaster_recovery','excel','power_bi','documentation','rc1_evidence')
CRITICAL=('ci','regression','security','disaster_recovery')
def _id(*parts:Any)->str:
    return 'GOVGO-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:12].upper()
def execute_final_go(evidence:dict[str,Any], approvals:dict[str,Any], release:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
    rules=rules or {}; required=tuple(rules.get('required_evidence',REQUIRED)); critical=set(rules.get('critical_evidence',CRITICAL)); rows=[]
    target_commit=str(release.get('commit_sha') or ''); version=str(release.get('version') or ''); tag=str(release.get('tag') or '')
    for name in required:
        raw=evidence.get(name,{}) if isinstance(evidence.get(name,{}),dict) else {'closed':bool(evidence.get(name))}
        passed=bool(raw.get('passed',raw.get('closed',False))); verified=bool(raw.get('verified',passed)); ref=raw.get('evidence_ref'); commit=str(raw.get('commit_sha') or '')
        commit_ok=(not commit) or (not target_commit) or commit==target_commit
        closed=passed and verified and bool(ref) and commit_ok
        rows.append({'evidence':name,'passed':passed,'verified':verified,'evidence_ref':ref,'commit_sha':commit or None,'commit_matches_release':commit_ok,'critical':name in critical,'closed':closed})
    closed_count=sum(r['closed'] for r in rows); closure_pct=round(100*closed_count/len(rows),1) if rows else 0.0
    critical_blockers=[r['evidence'] for r in rows if r['critical'] and not r['closed']]; open_items=[r['evidence'] for r in rows if not r['closed']]
    security_ok=bool(approvals.get('security_owner_approved',False)); release_ok=bool(approvals.get('release_owner_approved',False)); board_ok=bool(approvals.get('board_go_no_go_confirmed',False)); approvals_ok=security_ok and release_ok and board_ok
    identity_ok=bool(version and target_commit and tag); min_closure=float(rules.get('minimum_evidence_closure_pct',100)); evidence_ok=closure_pct>=min_closure and not open_items
    if critical_blockers: decision='NO-GO'
    elif not evidence_ok or not approvals_ok or not identity_ok: decision='HOLD'
    else: decision='GO'
    execution_id=_id(version,target_commit,tag,decision,closure_pct)
    return {'production_release_evidence_closure_final_go_version':ENGINE_VERSION,'final_go_execution_id':execution_id,'decision':decision,'evidence_closure_pct':closure_pct,'evidence_matrix':rows,'critical_blockers':critical_blockers,'open_items':open_items,'all_required_approvals':approvals_ok,'release_identity_complete':identity_ok,'production_release_authorized':decision=='GO','release_tag_authorized':decision=='GO','immutable_evidence_archive_required':decision=='GO','manual_release_execution_required':decision=='GO','automatic_release':False,'automatic_evidence_waiver':False,'automatic_approval':False,'release_manifest':{'execution_id':execution_id,'version':version,'target_commit_sha':target_commit,'release_tag':tag,'decision':decision,'evidence_closure_pct':closure_pct,'evidence_refs':{r['evidence']:r['evidence_ref'] for r in rows if r['closed']},'approvals':{'security_owner':security_ok,'release_owner':release_ok,'go_no_go_board':board_ok}},'next_action':'Voer handmatig release-tag en productie-release uit en archiveer het bewijs immutable.' if decision=='GO' else ('Sluit ontbrekend bewijs/goedkeuringen/release-identiteit en voer Final GO opnieuw uit.' if decision=='HOLD' else 'Herstel kritieke blockers en voer alle productiepoorten opnieuw uit.')}
