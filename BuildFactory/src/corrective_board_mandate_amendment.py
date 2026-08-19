"""Enterprise 9.7 Corrective Board Decision & Strategic Mandate Amendment."""
from __future__ import annotations
from copy import deepcopy
from hashlib import sha256
from typing import Any

ENGINE_VERSION='9.7.0'
APPROVED={'GOEDGEKEURD','AKKOORD','APPROVED'}

def _id(prefix:str,*parts:Any)->str:
    raw='|'.join(str(x) for x in parts)
    return f"{prefix}-{sha256(raw.encode()).hexdigest()[:10].upper()}"

def build_corrective_board_mandate_amendment(corrective_optimizer:dict[str,Any], board_mandate:dict[str,Any], existing:dict[str,Any]|None=None)->dict[str,Any]:
    existing=existing or {}
    ranking=corrective_optimizer.get('ranking',[]) or []
    mandate=deepcopy(board_mandate.get('mandate',{}) or {})
    if not ranking or not mandate:
        return {'corrective_board_mandate_amendment_version':ENGINE_VERSION,'status':'GEEN WIJZIGING BESCHIKBAAR','decision':{},'amendment':{},'amended_mandate':mandate,'next_action':'Genereer eerst een correctievoorstel op een actief strategisch mandaat.'}
    prior=existing.get('decision',{}) or {}
    selected_rank=int(prior.get('selected_rank',ranking[0].get('rank',1)) or 1)
    selected=next((r for r in ranking if int(r.get('rank',0))==selected_rank),ranking[0])
    decision_status=str(prior.get('decision','BESLUIT VEREIST')).upper()
    decision_id=prior.get('decision_id') or _id('PCD',mandate.get('mandate_id',''),selected_rank)
    decision={'decision_id':decision_id,'selected_rank':selected_rank,'decision':decision_status,'approved_by':prior.get('approved_by',''),'approved_at':prior.get('approved_at',''),'rationale':prior.get('rationale',''),'decision_authority':prior.get('decision_authority','Bestuur/ALV'),'selected_corrective_action':selected}
    if decision_status not in APPROVED:
        return {'corrective_board_mandate_amendment_version':ENGINE_VERSION,'status':'BESLUIT VEREIST','decision':decision,'amendment':{},'amended_mandate':mandate,'human_approval_required':True,'automatic_execution':False,'next_action':'Laat Bestuur/ALV de gekozen herstelroute formeel goedkeuren.'}
    action=selected.get('action',{}) or {}
    amendment_id=(existing.get('amendment',{}) or {}).get('amendment_id') or _id('PSMA',decision_id,mandate.get('mandate_id',''))
    amended=deepcopy(mandate)
    amended['amendment_id']=amendment_id
    amended['amendment_decision_id']=decision_id
    amended['status']='GEWIJZIGD ACTIEF'
    amended['mjop_acceleration']=round(float(amended.get('mjop_acceleration',0) or 0)+float(action.get('extra_mjop_acceleration',0) or 0),4)
    amended['sustainability_investment']=round(float(amended.get('sustainability_investment',0) or 0)+float(action.get('sustainability_adjustment',0) or 0),4)
    amended['investment_budget_36m']=round(float(amended.get('investment_budget_36m',0) or 0)*(1-float(action.get('budget_reduction_pct',0) or 0))+float(selected.get('estimated_corrective_cost',0) or 0),2)
    contribution_extra=float(action.get('extra_contribution_delta',0) or 0)
    amended['contribution_path']=[{**x,'contribution_delta':round(float(x.get('contribution_delta',0) or 0)+contribution_extra,4)} for x in amended.get('contribution_path',[]) or []]
    projected=float(selected.get('projected_governance_score',0) or 0)
    old_targets=amended.get('kpi_targets',[]) or []
    amended['kpi_targets']=[{**x,'target_score':round(max(float(x.get('target_score',0) or 0),projected if int(x.get('month',0))>=12 else float(x.get('target_score',0) or 0)),1)} for x in old_targets]
    amendment={'amendment_id':amendment_id,'base_mandate_id':mandate.get('mandate_id',''),'decision_id':decision_id,'selected_rank':selected_rank,'changes':{'extra_contribution_delta':contribution_extra,'extra_mjop_acceleration':action.get('extra_mjop_acceleration',0),'budget_reduction_pct':action.get('budget_reduction_pct',0),'sustainability_adjustment':action.get('sustainability_adjustment',0),'estimated_corrective_cost':selected.get('estimated_corrective_cost',0)},'new_kpi_targets':amended.get('kpi_targets',[]),'audit_trail_required':True}
    history=list(existing.get('amendment_history',[]) or [])
    if not any(x.get('amendment_id')==amendment_id for x in history): history.append(amendment)
    return {'corrective_board_mandate_amendment_version':ENGINE_VERSION,'status':'MANDAATWIJZIGING GOEDGEKEURD','decision':decision,'amendment':amendment,'amended_mandate':amended,'amendment_history':history,'human_approval_required':True,'automatic_execution':False,'automatic_financing_commitment':False,'next_action':'Vervang het actieve mandaat gecontroleerd door de goedgekeurde versie en hervat variance-control op de nieuwe targets.'}
