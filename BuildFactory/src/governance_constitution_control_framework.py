"""Enterprise 12.0 Governance Constitution & Strategic Control Framework."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='12.0.0'

def _id(prefix:str,*parts:Any)->str:
 return f"{prefix}-"+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()

def build_governance_constitution(doctrine:dict[str,Any], controls:dict[str,Any]|None=None, existing:dict[str,Any]|None=None)->dict[str,Any]:
 controls=controls or {}; existing=existing or {}; doctrines=doctrine.get('doctrines',[]) or []
 approved=[d for d in doctrines if str(d.get('status','')).upper() in {'GOEDGEKEURD','APPROVED','VASTGESTELD'} or bool(d.get('approved',False))]
 principles=[{'doctrine_id':d.get('doctrine_id'),'topic':d.get('topic'),'principle':d.get('strategic_principle'),'confidence':d.get('consistency_confidence')} for d in approved]
 authority=controls.get('authority_matrix',{'Bestuur':['dagelijks beheer','uitvoering binnen mandaat'],'ALV':['begroting','MJOP','materiele beleidswijziging','mandaat buiten bestuursgrens']})
 financial=controls.get('financial_limits',{'budget_variance_pct':0,'unapproved_commitment_eur':0,'reserve_floor_required':True})
 risk=controls.get('risk_rules',{'critical_requires_board_action':True,'red_requires_explicit_decision':True,'automatic_risk_acceptance':False})
 mjop=controls.get('mjop_rules',{'condition_and_risk_based':True,'lifecycle_cost_required':True,'deviation_requires_rationale':True})
 decision=controls.get('decision_rules',{'human_approval_required':True,'audit_trail_required':True,'precedent_check_required':True,'explainability_required':True})
 constitution_id=existing.get('constitution_id') or _id('GOVCONST',doctrine.get('baseline_id',''),len(principles))
 completeness=sum(bool(x) for x in (principles,authority,financial,risk,mjop,decision)); score=round(completeness/6*100,1)
 ready=bool(principles) and score==100
 return {'governance_constitution_control_framework_version':ENGINE_VERSION,'constitution_id':constitution_id,'status':'CONSTITUTIONEEL RAAMWERK GEREED VOOR VASTSTELLING' if ready else 'CONSTITUTIONEEL RAAMWERK ONVOLLEDIG','framework_completeness_score':score,'strategic_principles':principles,'authority_matrix':authority,'financial_limits':financial,'risk_rules':risk,'mjop_rules':mjop,'decision_rules':decision,'source_baseline_id':doctrine.get('baseline_id'),'human_constitution_approval_required':True,'human_legal_governance_review_required':True,'automatic_policy_change':False,'automatic_decision':False,'automatic_execution':False,'next_action':'Laat Bestuur/ALV het constitutionele raamwerk formeel toetsen en vaststellen.' if ready else 'Vul ontbrekende goedgekeurde doctrines en controleregels aan.'}
