"""Enterprise 11.3 Resolution Execution Compliance & Legal Governance Control.

Checks whether execution remains within the adopted resolution, mandate scope,
budget, authority and deadline. This is a governance control layer and not a
legal opinion.
"""
from __future__ import annotations
from datetime import date, datetime
from typing import Any
ENGINE_VERSION='11.3.0'

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _parse_date(v:Any):
    if not v:return None
    try:return datetime.fromisoformat(str(v)).date()
    except Exception:return None

def evaluate_resolution_execution_compliance(register:dict[str,Any], actuals:dict[str,Any]|None=None, today:date|None=None)->dict[str,Any]:
    actuals=actuals or {}; today=today or date.today()
    resolution=register.get('resolution',{}) or {}; mandate=register.get('execution_mandate',{}) or {}
    if register.get('status')!='BESLUIT AANGENOMEN - MANDAAT GEREED' or not resolution or not mandate:
        return {'resolution_execution_compliance_version':ENGINE_VERSION,'status':'GEEN ACTIEF UITVOERINGSMANDAAT','checks':{},'alerts':[],'automatic_execution':False}
    planned_budget=_num(mandate.get('budget'))
    actual_spend=_num(actuals.get('actual_spend',mandate.get('actual_spend',0)))
    budget_ok=True if planned_budget<=0 else actual_spend<=planned_budget
    expected_owner=str(mandate.get('owner','')).strip()
    actual_owner=str(actuals.get('owner',expected_owner)).strip()
    authority_ok=not expected_owner or actual_owner==expected_owner
    deadline=_parse_date(actuals.get('deadline',mandate.get('deadline')))
    completed=bool(actuals.get('completed',False) or _num(actuals.get('progress_pct',mandate.get('progress_pct',0)))>=100)
    deadline_ok=True if not deadline or completed else today<=deadline
    evidence=actuals.get('evidence',mandate.get('evidence',[])) or []
    evidence_ok=bool(evidence) if mandate.get('evidence_required',True) else True
    resolution_text=str(resolution.get('resolution_text','')).strip()
    execution_description=str(actuals.get('execution_description','')).strip()
    scope_attested=actuals.get('within_resolution_scope')
    scope_ok=bool(scope_attested) if scope_attested is not None else bool(resolution_text and execution_description and execution_description.lower() in resolution_text.lower())
    mandate_id_ok=str(actuals.get('mandate_id',mandate.get('mandate_id','')))==str(mandate.get('mandate_id',''))
    checks={'within_resolution_scope':scope_ok,'within_budget':budget_ok,'authorized_owner':authority_ok,'within_deadline':deadline_ok,'evidence_present':evidence_ok,'mandate_reference_valid':mandate_id_ok}
    alerts=[]
    if not scope_ok: alerts.append({'severity':'ROOD','type':'SCOPE','message':'Uitvoering valt mogelijk buiten de formele besluittekst of scope.'})
    if not budget_ok: alerts.append({'severity':'ROOD','type':'BUDGET','message':'Werkelijke besteding overschrijdt het gemandateerde budget.'})
    if not authority_ok: alerts.append({'severity':'ROOD','type':'AUTHORITY','message':'Uitvoering vindt plaats door een andere eigenaar dan gemandateerd.'})
    if not deadline_ok: alerts.append({'severity':'ORANJE','type':'DEADLINE','message':'Deadline is verstreken zonder aantoonbare voltooiing.'})
    if not evidence_ok: alerts.append({'severity':'ORANJE','type':'EVIDENCE','message':'Vereist uitvoeringsbewijs ontbreekt.'})
    if not mandate_id_ok: alerts.append({'severity':'ROOD','type':'MANDATE','message':'Uitvoering verwijst niet naar het geldige uitvoeringsmandaat.'})
    score=round(sum(1 for v in checks.values() if v)/len(checks)*100,1)
    status='CONFORM UITGEVOERD' if all(checks.values()) else ('KRITIEKE AFWIJKING' if any(a['severity']=='ROOD' for a in alerts) else 'AFWIJKING GEVONDEN')
    return {'resolution_execution_compliance_version':ENGINE_VERSION,'status':status,'compliance_score':score,'checks':checks,'alerts':alerts,'resolution_id':resolution.get('resolution_id',''),'mandate_id':mandate.get('mandate_id',''),'planned_budget':planned_budget,'actual_spend':actual_spend,'deadline':str(deadline) if deadline else '','human_legal_governance_review_required':status!='CONFORM UITGEVOERD','automatic_legal_opinion':False,'automatic_execution':False,'automatic_budget_commitment':False,'next_action':'Leg afwijkingen voor aan Bestuur/ALV en herstel of formaliseer een gewijzigd besluit/mandaat.' if alerts else 'Archiveer bewijs en sluit uitvoering bestuurlijk na menselijke controle.'}
