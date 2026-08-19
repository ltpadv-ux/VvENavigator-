"""Enterprise 9.4 Predictive Board Decision & Strategic Mandate."""
from __future__ import annotations
from hashlib import sha256
from typing import Any

ENGINE_VERSION='9.4.0'
APPROVED={'GOEDGEKEURD','AKKOORD','APPROVED'}

def _id(prefix:str,*parts:Any)->str:
    raw='|'.join(str(x) for x in parts)
    return f"{prefix}-{sha256(raw.encode()).hexdigest()[:10].upper()}"

def build_predictive_board_mandate(decision_portfolio:dict[str,Any], existing:dict[str,Any]|None=None)->dict[str,Any]:
    existing=existing or {}
    cards=decision_portfolio.get('board_choice_cards',[]) or []
    if not cards:
        return {'predictive_board_mandate_version':ENGINE_VERSION,'status':'GEEN KEUZE BESCHIKBAAR','decision':{},'mandate':{},'next_action':'Genereer eerst een Pareto-keuzekaart.'}
    prior=existing.get('decision',{}) or {}
    selected_label=prior.get('selected_label') or cards[0].get('label','')
    selected=next((c for c in cards if c.get('label')==selected_label),cards[0])
    decision_status=str(prior.get('decision','BESLUIT VEREIST')).upper()
    decision_id=prior.get('decision_id') or _id('PBD',selected_label,selected.get('pareto_rank',0))
    decision={'decision_id':decision_id,'selected_label':selected_label,'decision':decision_status,'approved_by':prior.get('approved_by',''),'approved_at':prior.get('approved_at',''),'rationale':prior.get('rationale',''),'decision_authority':prior.get('decision_authority','Bestuur/ALV'),'selected_option':selected}
    if decision_status not in APPROVED:
        return {'predictive_board_mandate_version':ENGINE_VERSION,'status':'BESLUIT VEREIST','decision':decision,'mandate':{},'human_approval_required':True,'automatic_execution':False,'next_action':'Laat Bestuur/ALV de gekozen Pareto-variant formeel goedkeuren.'}
    iv=selected.get('intervention',{}) or {}
    old_mandate=existing.get('mandate',{}) or {}
    mandate_id=old_mandate.get('mandate_id') or _id('PSM',decision_id,selected_label)
    monthly_path=[{'month':12,'contribution_delta':iv.get('contribution_delta',0)},{'month':24,'contribution_delta':iv.get('contribution_delta',0)},{'month':36,'contribution_delta':iv.get('contribution_delta',0)}]
    kpi_targets=[{'month':12,'target_score':selected.get('score_12m',0)},{'month':24,'target_score':selected.get('score_24m',0)},{'month':36,'target_score':selected.get('score_36m',0)}]
    mandate={'mandate_id':mandate_id,'decision_id':decision_id,'status':'ACTIEF','owner':old_mandate.get('owner','Bestuur / beheerder'),'contribution_path':monthly_path,'mjop_acceleration':iv.get('mjop_acceleration',0),'sustainability_investment':iv.get('sustainability_investment',0),'financing_share':iv.get('financing_share',0),'investment_budget_36m':selected.get('estimated_36m_cost',0),'risk_reduction_target':selected.get('risk_reduction',0),'sustainability_target':selected.get('sustainability_impact',0),'kpi_targets':kpi_targets,'measurement_months':[12,24,36],'evidence_required':True,'automatic_strategy_change':False,'automatic_financing_commitment':False}
    return {'predictive_board_mandate_version':ENGINE_VERSION,'status':'STRATEGISCH MANDAAT ACTIEF','decision':decision,'mandate':mandate,'human_approval_required':True,'automatic_execution':False,'next_action':'Wijs eigenaar toe, borg budget/financiering en meet KPI-doelen op 12, 24 en 36 maanden.'}
