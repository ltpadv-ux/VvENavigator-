"""Translate governance decisions into formal ALV decision proposals."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION="5.2.0"

def build_alv_workflow(register: dict[str,Any], financial_context: dict[str,Any]|None=None, existing: dict[str,Any]|None=None) -> dict[str,Any]:
    financial_context=financial_context or {}; previous={x.get('decision_id'):x for x in (existing or {}).get('items',[]) or []}; now=datetime.now(timezone.utc).isoformat(); items=[]
    for decision in register.get('decisions',[]) or []:
        did=str(decision.get('id','')); old=previous.get(did,{})
        monthly=float(financial_context.get('monthly_per_apartment',0.0) or 0.0); reserve=float(financial_context.get('reserve_impact',0.0) or 0.0)
        proposal=old.get('proposal_text') or f"De ALV wordt voorgesteld te besluiten over {decision.get('reason','de voorliggende governance-uitzondering')} en het bestuur mandaat te geven voor uitvoering binnen de vastgestelde kaders."
        items.append({"decision_id":did,"agenda_status":old.get('agenda_status','VOORBEREIDEN'),"proposal_text":proposal,"financial_consequence":{"monthly_per_apartment":monthly,"reserve_impact":reserve,"currency":"EUR"},"vote_status":old.get('vote_status','NIET GESTEMD'),"vote_result":old.get('vote_result','ONBEKEND'),"execution_order":old.get('execution_order','Na positief ALV-besluit uitvoeren door verantwoordelijke eigenaar.'),"owner":decision.get('owner','Bestuur / Beheerder'),"rationale":decision.get('rationale',''),"created_at":old.get('created_at',now),"updated_at":now})
    ready=sum(1 for x in items if x['agenda_status']=='GEREED VOOR ALV'); decided=sum(1 for x in items if x['vote_status']=='AFGEROND')
    return {"alv_decision_workflow_version":ENGINE_VERSION,"generated_at":now,"item_count":len(items),"ready_for_alv":ready,"decided_count":decided,"items":items,"status":"GEREED" if items and ready==len(items) else "VOORBEREIDEN" if items else "GEEN BESLUITEN","next_action":"Agendeer de gereedstaande voorstellen voor de ALV." if items else "Geen ALV-besluit nodig."}
