"""Enterprise 14.3 Financial Resolution Execution Mandate & Budget Lock Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='14.3.0'

def _id(*parts:Any)->str:return 'GOVMND-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def create_execution_mandate(validation:dict[str,Any], pack:dict[str,Any], execution:dict[str,Any]|None=None)->dict[str,Any]:
 execution=execution or {}; preferred=pack.get('preferred_path') or {}; validated=bool(validation.get('validated_for_formal_registration',False))
 budget=_num(execution.get('approved_budget_eur',preferred.get('source_cost_eur',preferred.get('cost_eur',0)))); reserve_draw=_num(execution.get('approved_reserve_draw_eur',preferred.get('reserve_draw_eur',0))); monthly=_num(execution.get('approved_monthly_extra_eur',preferred.get('maximum_monthly_extra_eur',0))); term=int(_num(execution.get('term_months',preferred.get('term_months',0))) or 0); tolerance=max(0,_num(execution.get('budget_tolerance_pct',0)))
 owner=str(execution.get('responsible_owner','')).strip(); resolution_ref=str(execution.get('formal_resolution_reference','')).strip(); contribution_path=str(execution.get('contribution_path',preferred.get('scenario_name',''))).strip()
 blockers=[]
 if not validated:blockers.append('ALV-besluit is nog niet gevalideerd voor formele registratie.')
 if budget<=0:blockers.append('Goedgekeurd uitvoeringsbudget ontbreekt of is nul.')
 if not owner:blockers.append('Verantwoordelijke uitvoerder/eigenaar ontbreekt.')
 if not resolution_ref:blockers.append('Formele besluitreferentie ontbreekt.')
 if term<=0:blockers.append('Looptijd van het bijdrage-/uitvoeringspad ontbreekt.')
 locked=validated and not blockers; max_commitment=round(budget*(1+tolerance/100),2)
 return {'financial_resolution_execution_mandate_budget_lock_version':ENGINE_VERSION,'mandate_id':_id(validation.get('validation_id',''),resolution_ref,budget),'status':'UITVOERINGSMANDAAT GEREED & BUDGET GEBLOKKEERD' if locked else 'UITVOERINGSMANDAAT ONVOLLEDIG / GEBLOKKEERD','formal_resolution_reference':resolution_ref,'responsible_owner':owner,'contribution_path':contribution_path,'term_months':term,'approved_budget_eur':round(budget,2),'budget_tolerance_pct':round(tolerance,2),'maximum_commitment_eur':max_commitment,'approved_reserve_draw_eur':round(reserve_draw,2),'approved_monthly_extra_eur':round(monthly,2),'budget_lock_active':locked,'spend_outside_mandate_blocked':True,'change_requires_new_approval':True,'blockers':blockers,'source_validation_id':validation.get('validation_id'),'source_resolution_pack_id':pack.get('resolution_pack_id'),'human_execution_authorization_required':True,'human_budget_owner_confirmation_required':True,'automatic_spend':False,'automatic_reserve_draw':False,'automatic_contribution_change':False,'automatic_execution':False,'next_action':'Activeer uitvoering pas na formele mandaatbevestiging; toets elke verplichting aan budget, looptijd en besluitreferentie.' if locked else 'Vul de ontbrekende mandaatvelden aan of rond eerst de ALV-validatie af.'}

def validate_commitment(mandate:dict[str,Any], commitment_eur:float, cumulative_committed_eur:float=0)->dict[str,Any]:
 amount=max(0,_num(commitment_eur)); cumulative=max(0,_num(cumulative_committed_eur)); maximum=_num(mandate.get('maximum_commitment_eur',0)); active=bool(mandate.get('budget_lock_active',False)); projected=round(cumulative+amount,2); allowed=active and projected<=maximum
 return {'mandate_id':mandate.get('mandate_id'),'commitment_eur':round(amount,2),'cumulative_before_eur':round(cumulative,2),'projected_cumulative_eur':projected,'maximum_commitment_eur':round(maximum,2),'allowed_within_budget_lock':allowed,'status':'TOEGESTAAN BINNEN MANDAAT' if allowed else 'GEBLOKKEERD BUITEN MANDAAT','automatic_commitment':False}
