"""Enterprise 12.8 Constitutional Activation & Cutover Control."""
from __future__ import annotations
from datetime import date
from hashlib import sha256
from typing import Any
ENGINE_VERSION='12.8.0'
APPROVED={'GOEDGEKEURD','VASTGESTELD','APPROVED','AANGENOMEN'}

def _id(*parts:Any)->str:return 'GOVCUT-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()

def prepare_constitutional_cutover(impact:dict[str,Any], version_result:dict[str,Any], approval:dict[str,Any]|None=None, existing:dict[str,Any]|None=None)->dict[str,Any]:
 approval=approval or {}; existing=existing or {}; current=version_result.get('current_version',{}) or {}
 if not impact.get('activation_ready',False):
  return {'constitutional_activation_cutover_control_version':ENGINE_VERSION,'status':'CUTOVER GEBLOKKEERD - MIGRATIES OPEN','cutover':{},'automatic_activation':False}
 new_version=str(version_result.get('new_version',current.get('version',''))); previous=str(version_result.get('previous_version',''))
 approval_status=str(approval.get('approval_status',existing.get('approval_status','CONCEPT'))).upper(); authority=str(approval.get('decision_authority',existing.get('decision_authority',''))).strip(); resolution=str(approval.get('resolution_reference',existing.get('resolution_reference',''))).strip(); cutover_date=str(approval.get('cutover_date',existing.get('cutover_date',date.today()))).strip(); review_date=str(approval.get('post_activation_review_date',existing.get('post_activation_review_date',''))).strip(); evidence=list(approval.get('activation_evidence',existing.get('activation_evidence',[])) or [])
 rollback=str(approval.get('rollback_version',existing.get('rollback_version',previous))).strip(); complete=bool(new_version and authority and resolution and cutover_date and review_date and rollback and evidence); approved=complete and approval_status in APPROVED
 cutover_id=existing.get('cutover_id') or _id(new_version,previous,resolution)
 record={'cutover_id':cutover_id,'new_version':new_version,'previous_version':previous,'rollback_version':rollback,'approval_status':approval_status,'decision_authority':authority,'resolution_reference':resolution,'cutover_date':cutover_date,'post_activation_review_date':review_date,'activation_evidence':evidence,'migration_id':impact.get('migration_id'),'affected_item_count':impact.get('affected_item_count',0),'financial_exposure_eur':impact.get('financial_exposure_eur',0),'human_activation_approval_required':True}
 return {'constitutional_activation_cutover_control_version':ENGINE_VERSION,'status':'CUTOVER GEREED VOOR FORMELE ACTIVATIE' if approved else 'CUTOVER CONCEPT / ONVOLLEDIG','cutover':record,'activation_ready':approved,'rollback_ready':bool(rollback),'human_legal_governance_review_required':True,'automatic_activation':False,'automatic_rollback':False,'automatic_decision':False,'next_action':'Voer formele activatie uit en plan post-activation review.' if approved else 'Leg goedkeuring, besluitreferentie, cutoverdatum, rollback-versie, bewijs en reviewdatum vast.'}
