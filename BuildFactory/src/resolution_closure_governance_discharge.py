"""Enterprise 11.4 Resolution Closure & Governance Discharge.

Formally closes an adopted resolution only when execution, evidence, financial
outcome and governance review are complete. It supports governance discharge;
it does not create legal discharge by itself.
"""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='11.4.0'
APPROVED={'GOEDGEKEURD','AKKOORD','APPROVED','DECHARGE VERLEEND','VERLEEND'}

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _id(prefix:str,*parts:Any)->str:
    return f"{prefix}-"+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()

def close_resolution_and_discharge(register:dict[str,Any], compliance:dict[str,Any], closure:dict[str,Any]|None=None, existing:dict[str,Any]|None=None)->dict[str,Any]:
    closure=closure or {}; existing=existing or {}
    resolution=register.get('resolution',{}) or {}; mandate=register.get('execution_mandate',{}) or {}
    if register.get('status')!='BESLUIT AANGENOMEN - MANDAAT GEREED' or not resolution or not mandate:
        return {'resolution_closure_governance_discharge_version':ENGINE_VERSION,'status':'GEEN SLUITBAAR BESLUIT','closure':{},'discharge':{},'automatic_discharge':False}
    compliance_ok=compliance.get('status')=='CONFORM UITGEVOERD' and not (compliance.get('alerts',[]) or [])
    progress=_num(closure.get('progress_pct',mandate.get('progress_pct',0)))
    completed=bool(closure.get('completed',progress>=100))
    evidence=closure.get('evidence',mandate.get('evidence',[])) or []
    evidence_ok=bool(evidence)
    budget=_num(mandate.get('budget')); actual=_num(closure.get('actual_spend',compliance.get('actual_spend',mandate.get('actual_spend',0))))
    financial_ok=True if budget<=0 else actual<=budget
    delivery_note=str(closure.get('delivery_note','')).strip(); delivery_ok=bool(delivery_note)
    final_result=str(closure.get('final_result','')).strip(); result_ok=bool(final_result)
    governance_review=str(closure.get('governance_review','')).upper(); review_ok=governance_review in APPROVED
    checks={'execution_compliant':compliance_ok,'execution_complete':completed,'evidence_complete':evidence_ok,'financial_result_within_mandate':financial_ok,'delivery_documented':delivery_ok,'final_result_documented':result_ok,'governance_review_approved':review_ok}
    ready=all(checks.values())
    prior=existing.get('closure',{}) or {}
    closure_id=prior.get('closure_id') or _id('ALVCLS',resolution.get('resolution_id',''),mandate.get('mandate_id',''))
    closure_record={'closure_id':closure_id,'resolution_id':resolution.get('resolution_id',''),'mandate_id':mandate.get('mandate_id',''),'progress_pct':progress,'completed':completed,'planned_budget':budget,'actual_spend':actual,'financial_variance':round(actual-budget,2) if budget else 0.0,'delivery_note':delivery_note,'final_result':final_result,'evidence':evidence,'checks':checks,'status':'SLUITING GEREED' if ready else 'SLUITING ONVOLLEDIG'}
    discharge={}
    if ready:
        old=existing.get('discharge',{}) or {}
        discharge_id=old.get('discharge_id') or _id('ALVDCH',closure_id,resolution.get('minutes_reference',''))
        discharge={'discharge_id':discharge_id,'closure_id':closure_id,'resolution_id':resolution.get('resolution_id',''),'status':'DECHARGE VOORSTEL GEREED','approved_by':old.get('approved_by',closure.get('approved_by','')),'approved_at':old.get('approved_at',closure.get('approved_at','')),'minutes_reference':old.get('minutes_reference',closure.get('minutes_reference',resolution.get('minutes_reference',''))),'remarks':old.get('remarks',closure.get('remarks','')),'human_approval_required':True}
    status='SLUITING & DECHARGE GEREED' if ready else ('KRITIEKE AFWIJKING - NIET SLUITEN' if compliance.get('status')=='KRITIEKE AFWIJKING' else 'SLUITING NOG NIET GEREED')
    return {'resolution_closure_governance_discharge_version':ENGINE_VERSION,'status':status,'closure':closure_record,'discharge':discharge,'human_governance_discharge_required':True,'human_legal_validation_required':True,'automatic_discharge':False,'automatic_closure':False,'next_action':'Laat Bestuur/ALV decharge formeel vastleggen en archiveer het complete dossier.' if ready else 'Rond ontbrekende uitvoering, bewijs, financieel resultaat of governance-review af voordat decharge wordt overwogen.'}
