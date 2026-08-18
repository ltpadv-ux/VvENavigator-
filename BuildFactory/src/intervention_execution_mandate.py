"""Human approval workflow that converts a ranked intervention into a controlled execution mandate."""
from __future__ import annotations
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

ENGINE_VERSION='6.8.0'
APPROVED={'GOEDGEKEURD','APPROVED'}

def _id(prefix:str,*parts:Any)->str:
    raw='|'.join(str(x) for x in parts); return f"{prefix}-{sha256(raw.encode()).hexdigest()[:10].upper()}"

def build_intervention_execution_mandate(matrix:dict[str,Any], existing:dict[str,Any]|None=None)->dict[str,Any]:
    existing=existing or {}; now=datetime.now(timezone.utc).isoformat(); ranking=matrix.get('ranking',[]) or []
    preferred=ranking[0] if ranking else {}
    if not preferred:
        return {'intervention_execution_mandate_version':ENGINE_VERSION,'generated_at':now,'status':'GEEN BESLUIT NODIG','decision':{},'mandate':{},'next_action':'Geen interventievariant beschikbaar.'}
    previous=existing.get('decision',{}) or {}; selected=previous.get('selected_option') or preferred.get('option',''); selected_row=next((r for r in ranking if r.get('option')==selected),preferred)
    decision_status=str(previous.get('decision','BESLUIT VEREIST')).upper(); approved=decision_status in APPROVED
    decision_id=previous.get('decision_id') or _id('INTDEC',selected_row.get('intervention_id',''),selected)
    decision={'decision_id':decision_id,'selected_option':selected,'intervention_id':selected_row.get('intervention_id',''),'decision':decision_status,'approved_by':previous.get('approved_by',''),'approved_at':previous.get('approved_at',''),'rationale':previous.get('rationale',''),'decision_authority':selected_row.get('decision_authority','Bestuur/ALV'),'recommended_rank':selected_row.get('rank',0),'recommended_score':selected_row.get('weighted_score',0)}
    if not approved:
        return {'intervention_execution_mandate_version':ENGINE_VERSION,'generated_at':now,'status':'BESLUIT VEREIST','decision':decision,'mandate':{},'human_approval_required':True,'automatic_execution':False,'next_action':f"Laat {decision['decision_authority']} de gekozen interventie formeel goedkeuren."}
    impact=selected_row.get('impact',{}) or {}; mandate_id=(existing.get('mandate',{}) or {}).get('mandate_id') or _id('INTMAN',decision_id,selected)
    mandate={'mandate_id':mandate_id,'decision_id':decision_id,'status':'ACTIEF','owner':(existing.get('mandate',{}) or {}).get('owner','Bestuur / beheerder'),'option':selected,'domain':selected_row.get('domain',''),'kpi':selected_row.get('kpi',''),'budget_ceiling':round(float(((impact.get('horizons',{}) or {}).get('30',{}) or {}).get('lcc',0) or 0),2),'projected_reserve':impact.get('projected_reserve',0),'monthly_contribution_per_apartment':impact.get('monthly_contribution_per_apartment',0),'mjop_shift_months':impact.get('mjop_shift_months',0),'target_risk_delta':impact.get('risk_score_delta',0),'execution_deadline':(existing.get('mandate',{}) or {}).get('execution_deadline',''),'effect_measurement_required':True,'effect_kpis':['budget_ceiling','reserve','monthly_contribution','mjop_shift','risk_delta'],'created_at':(existing.get('mandate',{}) or {}).get('created_at',now)}
    return {'intervention_execution_mandate_version':ENGINE_VERSION,'generated_at':now,'status':'MANDAAT ACTIEF','decision':decision,'mandate':mandate,'human_approval_required':True,'automatic_execution':False,'next_action':'Wijs eigenaar en deadline toe, voer binnen mandaat uit en meet het effect.'}
