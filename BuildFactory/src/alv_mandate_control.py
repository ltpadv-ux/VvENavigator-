"""Execution mandate control for approved ALV decisions."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import hashlib

ENGINE_VERSION="5.3.0"
APPROVED_RESULTS={"AANGENOMEN","GOEDGEKEURD","AKKOORD","BESLOTEN"}

def _mandate_id(decision_id:str)->str:
    return "MAN-"+hashlib.sha256(decision_id.encode()).hexdigest()[:10].upper()

def build_execution_mandates(workflow: dict[str,Any], existing: dict[str,Any]|None=None) -> dict[str,Any]:
    previous={x.get('decision_id'):x for x in (existing or {}).get('mandates',[]) or []}; now=datetime.now(timezone.utc).isoformat(); mandates=[]
    for item in workflow.get('items',[]) or []:
        vote_status=str(item.get('vote_status','')).upper(); vote_result=str(item.get('vote_result','')).upper(); approved=vote_status=='AFGEROND' and vote_result in APPROVED_RESULTS
        if not approved: continue
        did=str(item.get('decision_id','')); old=previous.get(did,{})
        fin=item.get('financial_consequence',{}) or {}; budget=float(old.get('budget',fin.get('reserve_impact',0.0)) or 0.0)
        mandates.append({"mandate_id":old.get('mandate_id',_mandate_id(did)),"decision_id":did,"owner":old.get('owner',item.get('owner','Bestuur / Beheerder')),"mandate_text":old.get('mandate_text',item.get('execution_order','Voer het ALV-besluit uit binnen de vastgestelde kaders.')),"budget":budget,"currency":"EUR","deadline":old.get('deadline',''),"status":old.get('status','OPEN'),"progress_percent":int(old.get('progress_percent',0) or 0),"spent_amount":float(old.get('spent_amount',0.0) or 0.0),"reporting_note":old.get('reporting_note',''),"created_at":old.get('created_at',now),"updated_at":now})
    open_count=sum(str(x['status']).upper() not in {'GEREED','AFGEROND','CLOSED'} for x in mandates)
    total_budget=round(sum(float(x.get('budget',0) or 0) for x in mandates),2); total_spent=round(sum(float(x.get('spent_amount',0) or 0) for x in mandates),2)
    return {"alv_mandate_control_version":ENGINE_VERSION,"generated_at":now,"mandate_count":len(mandates),"open_count":open_count,"total_budget":total_budget,"total_spent":total_spent,"budget_remaining":round(total_budget-total_spent,2),"mandates":mandates,"status":"ACTIE VEREIST" if open_count else "BIJGEWERKT","next_action":mandates[0].get('mandate_text','Geen uitvoeringsmandaat') if open_count and mandates else "Geen open uitvoeringsmandaten."}
