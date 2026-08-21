"""Enterprise 19.0 Final Enterprise Production Baseline & Handover Pack."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='19.0.0'
REQUIRED_DOCS=('architecture','operations_runbook','security_runbook','backup_restore_runbook','release_runbook','data_dictionary','excel_guide','power_bi_guide','governance_guide','incident_response','change_management')
def _id(*p:Any)->str:return 'GOVHND-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:12].upper()
def build_handover_pack(baseline:dict[str,Any], docs:dict[str,Any], approvals:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; required=tuple(rules.get('required_documents',REQUIRED_DOCS)); version=str(baseline.get('version') or ''); commit=str(baseline.get('commit_sha') or ''); tag=str(baseline.get('tag') or ''); release_record=baseline.get('ga_release_record_ref'); assurance_ref=baseline.get('continuous_assurance_ref'); rows=[]
 for name in required:
  raw=docs.get(name,{}) if isinstance(docs.get(name,{}),dict) else {'present':bool(docs.get(name))}; present=bool(raw.get('present',False)); verified=bool(raw.get('verified',present)); ref=raw.get('reference'); rows.append({'document':name,'present':present,'verified':verified,'reference':ref,'closed':present and verified and bool(ref)})
 open_docs=[r['document'] for r in rows if not r['closed']]; doc_pct=round(100*sum(r['closed'] for r in rows)/len(rows),1) if rows else 0.0
 identity_ok=bool(version and commit and tag and release_record and assurance_ref); approvals_ok=all(bool(approvals.get(k,False)) for k in ('product_owner_approved','operations_owner_approved','security_owner_approved','business_owner_approved'))
 baseline_frozen=bool(baseline.get('baseline_frozen',False)); release_freeze=bool(baseline.get('release_freeze_enabled',False)); handover_complete=doc_pct>=float(rules.get('minimum_documentation_pct',100)) and not open_docs and identity_ok and approvals_ok and baseline_frozen and release_freeze
 decision='HANDOVER ACCEPTED' if handover_complete else 'HANDOVER HOLD'
 pack_id=_id(version,commit,tag,decision,doc_pct)
 return {'final_enterprise_production_baseline_handover_version':ENGINE_VERSION,'handover_pack_id':pack_id,'decision':decision,'documentation_closure_pct':doc_pct,'documentation_matrix':rows,'open_documents':open_docs,'baseline_identity_complete':identity_ok,'baseline_frozen':baseline_frozen,'release_freeze_enabled':release_freeze,'all_required_approvals':approvals_ok,'handover_complete':handover_complete,'steady_state_operations_authorized':handover_complete,'automatic_baseline_change':False,'automatic_release_unfreeze':False,'handover_pack':{'id':pack_id,'version':version,'commit_sha':commit,'tag':tag,'ga_release_record_ref':release_record,'continuous_assurance_ref':assurance_ref,'document_refs':{r['document']:r['reference'] for r in rows if r['closed']},'approvals':{k:bool(approvals.get(k,False)) for k in ('product_owner_approved','operations_owner_approved','security_owner_approved','business_owner_approved')}},'next_action':'Archiveer het handover pack en beheer wijzigingen vanaf nu uitsluitend via formeel change management.' if handover_complete else 'Sluit ontbrekende documentatie, approvals, baseline freeze of release freeze vóór overdracht.'}
