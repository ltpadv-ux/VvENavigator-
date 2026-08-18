"""Apply approved corrective decisions to execution mandates with before/after history."""
from __future__ import annotations
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
from typing import Any

ENGINE_VERSION="5.8.0"


def _shift_deadline(deadline:str, days:int)->str:
    if not deadline or not days: return deadline
    try: return (date.fromisoformat(deadline[:10])+timedelta(days=days)).isoformat()
    except ValueError: return deadline


def apply_mandate_amendments(mandates:dict[str,Any], amendments:list[dict[str,Any]], existing_history:dict[str,Any]|None=None)->dict[str,Any]:
    now=datetime.now(timezone.utc).isoformat(); history=list((existing_history or {}).get('history',[]) or []); by_id={str(x.get('mandate_id','')):dict(x) for x in mandates.get('mandates',[]) or []}; applied=[]
    seen={(str(x.get('corrective_id','')),str(x.get('mandate_id',''))) for x in history}
    for a in amendments:
        key=(str(a.get('corrective_id','')),str(a.get('mandate_id','')))
        if key in seen: continue
        mid=key[1]; mandate=by_id.get(mid)
        if not mandate: continue
        before=deepcopy(mandate); action=str(a.get('action','')).upper(); budget_change=float(a.get('budget_change',0) or 0); schedule_days=int(a.get('schedule_change_days',0) or 0)
        if budget_change: mandate['budget']=round(float(mandate.get('budget',0) or 0)+budget_change,2)
        if schedule_days: mandate['deadline']=_shift_deadline(str(mandate.get('deadline','')),schedule_days)
        if action=='SCOPE_AANPASSEN': mandate['scope_status']='AANGEPAST'; mandate['scope_change_note']=a.get('rationale','Goedgekeurde scope-aanpassing')
        elif action=='FASEREN': mandate['phasing_status']='GEFASEERD'; mandate['phasing_note']=a.get('rationale','Goedgekeurde fasering')
        mandate['last_corrective_id']=a.get('corrective_id',''); mandate['amended_at']=now; mandate['amendment_version']=int(mandate.get('amendment_version',0) or 0)+1
        after=deepcopy(mandate); record={"corrective_id":key[0],"mandate_id":mid,"action":action,"before":before,"after":after,"approved_by":a.get('approved_by',''),"approved_at":a.get('approved_at',''),"applied_at":now}; history.append(record); applied.append(record); by_id[mid]=mandate
    updated=[by_id.get(str(x.get('mandate_id','')),x) for x in mandates.get('mandates',[]) or []]
    return {"mandate_amendment_version":ENGINE_VERSION,"generated_at":now,"status":"AMENDEMENT TOEGEPAST" if applied else "GEEN NIEUW AMENDEMENT","applied_count":len(applied),"mandates":{**mandates,"mandates":updated},"applied":applied,"history":history,"next_action":"Voer na wijziging compliance- en forecastcontrole opnieuw uit." if applied else "Geen goedgekeurde nieuwe mandaatwijziging."}
