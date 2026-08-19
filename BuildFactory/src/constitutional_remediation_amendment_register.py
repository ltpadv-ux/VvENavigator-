"""Enterprise 12.5 Constitutional Remediation Decision & Amendment Register."""
from __future__ import annotations
from datetime import date
from hashlib import sha256
from typing import Any
ENGINE_VERSION='12.5.0'
APPROVED={'GOEDGEKEURD','VASTGESTELD','APPROVED','AANGENOMEN'}

def _id(prefix:str,*parts:Any)->str:return f"{prefix}-"+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def register_remediation_amendment(remediation:dict[str,Any], decision:dict[str,Any], current_framework:dict[str,Any]|None=None, existing:dict[str,Any]|None=None)->dict[str,Any]:
 current_framework=current_framework or {}; existing=existing or {}; actions=remediation.get('actions',[]) or []
 action_type=str(decision.get('action_type','')).upper(); selected=next((x for x in actions if str(x.get('type','')).upper()==action_type),None)
 approval=str(decision.get('approval_status','CONCEPT')).upper(); authority=str(decision.get('decision_authority','')).strip(); rationale=str(decision.get('rationale','')).strip(); resolution_ref=str(decision.get('resolution_reference','')).strip(); effective=str(decision.get('effective_date',date.today())).strip(); review=str(decision.get('review_date','')).strip()
 complete=bool(selected and authority and rationale and resolution_ref and effective and review); approved=complete and approval in APPROVED
 amendment_id=existing.get('amendment_id') or _id('GOVAMD',remediation.get('debt_score',''),action_type,resolution_ref)
 target='WAIVER_REGISTER' if action_type in {'WAIVER_TERMINATE_OR_REVIEW','CLOSE_EXPIRED_WAIVERS','COMPLETE_OVERDUE_REVIEWS'} else ('STRATEGIC_DOCTRINE' if action_type in {'NORMALIZE_REPEATED_EXCEPTION','DOCTRINE_REVIEW'} else 'GOVERNANCE_CONSTITUTION')
 version_from=str(current_framework.get('version',current_framework.get('governance_constitution_control_framework_version',''))); version_to=str(decision.get('target_version','')).strip()
 status='AMENDMENT GOEDGEKEURD VOOR GECONTROLEERDE VERWERKING' if approved else 'AMENDMENT CONCEPT / ONVOLLEDIG'
 record={'amendment_id':amendment_id,'action_type':action_type,'target':target,'scope':selected.get('scope','') if selected else '','approval_status':approval,'decision_authority':authority,'rationale':rationale,'resolution_reference':resolution_ref,'effective_date':effective,'review_date':review,'version_from':version_from,'version_to':version_to,'source_debt_level':remediation.get('debt_level'),'source_debt_score':remediation.get('debt_score'),'financial_impact_eur':selected.get('financial_impact_eur',0) if selected else 0,'audit_trace':{'remediation_version':remediation.get('constitutional_debt_remediation_version'),'constitution_id':current_framework.get('constitution_id','')}}
 return {'constitutional_remediation_amendment_register_version':ENGINE_VERSION,'status':status,'amendment':record,'ready_for_controlled_processing':approved,'human_approval_required':True,'human_legal_governance_review_required':True,'automatic_amendment_application':False,'automatic_policy_change':False,'automatic_constitution_change':False,'automatic_decision':False,'next_action':'Verwerk de goedgekeurde wijziging gecontroleerd met versiebeheer en leg de nieuwe baseline vast.' if approved else 'Selecteer een geldige herstelactie en leg bevoegdheid, motivering, besluitreferentie, ingangs- en reviewdatum vast.'}
