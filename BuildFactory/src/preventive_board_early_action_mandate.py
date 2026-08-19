"""Enterprise 10.5 Preventive Board Decision & Early Action Mandate."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='10.5.0'
APPROVED={'GOEDGEKEURD','AKKOORD','APPROVED'}

def _id(prefix:str,*parts:Any)->str:
    return f"{prefix}-"+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()

def build_preventive_board_early_action_mandate(simulator:dict[str,Any], existing:dict[str,Any]|None=None)->dict[str,Any]:
    existing=existing or {}
    recommended=simulator.get('recommended_scenario',{}) or {}
    if simulator.get('status')!='IMPACT PREVIEW BESCHIKBAAR' or not recommended:
        return {'preventive_board_early_action_mandate_version':ENGINE_VERSION,'status':'GEEN BESLUIT NODIG','decision':{},'mandate':{},'automatic_execution':False}
    prior=existing.get('decision',{}) or {}
    decision_status=str(prior.get('decision','BESLUIT VEREIST')).upper()
    scenario=str(prior.get('selected_scenario',recommended.get('scenario','VROEG INGRIJPEN')))
    decision_id=prior.get('decision_id') or _id('PBDP',scenario,simulator.get('trigger_alert_count',0),simulator.get('avoided_recovery_cost',0))
    decision={'decision_id':decision_id,'selected_scenario':scenario,'decision':decision_status,'approved_by':prior.get('approved_by',''),'approved_at':prior.get('approved_at',''),'rationale':prior.get('rationale',''),'decision_authority':prior.get('decision_authority','Bestuur/ALV')}
    if decision_status not in APPROVED:
        return {'preventive_board_early_action_mandate_version':ENGINE_VERSION,'status':'BESLUIT VEREIST','decision':decision,'mandate':{},'human_approval_required':True,'automatic_execution':False,'next_action':'Laat Bestuur/ALV de preventieve interventie formeel goedkeuren.'}
    chosen=next((x for x in simulator.get('scenarios',[]) if x.get('scenario')==scenario),recommended)
    mandate_prior=existing.get('mandate',{}) or {}
    mandate_id=mandate_prior.get('mandate_id') or _id('PEAM',decision_id,scenario)
    owner=mandate_prior.get('owner','Bestuur')
    budget=mandate_prior.get('budget',chosen.get('estimated_cost',0))
    deadline=mandate_prior.get('deadline','Binnen 3 maanden')
    measure_month=mandate_prior.get('measurement_month',chosen.get('horizon_months',12))
    target_health=mandate_prior.get('target_health_score',chosen.get('projected_health_score',0))
    target_risk=mandate_prior.get('target_risk_score',chosen.get('projected_risk_score',0))
    mandate={'mandate_id':mandate_id,'decision_id':decision_id,'status':'VROEG-ACTIEMANDAAT ACTIEF','scenario':scenario,'owner':owner,'budget':budget,'deadline':deadline,'measurement_month':measure_month,'target_health_score':target_health,'target_risk_score':target_risk,'expected_avoided_recovery_cost':simulator.get('avoided_recovery_cost',0),'evidence_required':True,'actual_spend':mandate_prior.get('actual_spend',0),'progress_pct':mandate_prior.get('progress_pct',0),'evidence':mandate_prior.get('evidence',[])}
    return {'preventive_board_early_action_mandate_version':ENGINE_VERSION,'status':'VROEG-ACTIEMANDAAT ACTIEF','decision':decision,'mandate':mandate,'human_approval_required':True,'automatic_execution':False,'automatic_budget_commitment':False,'next_action':'Voer de preventieve maatregel uit, verzamel bewijs en meet Health/Risk op het vastgelegde meetmoment.'}
