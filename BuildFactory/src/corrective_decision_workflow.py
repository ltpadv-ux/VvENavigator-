"""Turn corrective recommendations into auditable board/ALV approval decisions."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import hashlib

ENGINE_VERSION="5.7.0"

def _id(mandate_id:str, action:str)->str:
    return "COR-"+hashlib.sha256(f"{mandate_id}|{action}".encode()).hexdigest()[:10].upper()

def build_corrective_decisions(optimizer:dict[str,Any], existing:dict[str,Any]|None=None)->dict[str,Any]:
    old={x.get('corrective_id'):x for x in (existing or {}).get('decisions',[]) or []}; now=datetime.now(timezone.utc).isoformat(); decisions=[]
    for rec in optimizer.get('recommendations',[]) or []:
        best=rec.get('recommended_action',{}) or {}; cid=_id(str(rec.get('mandate_id','')),str(best.get('action','MONITOR'))); prev=old.get(cid,{})
        decision=prev.get('decision','NOG TE BESLUITEN'); status=prev.get('status','TER GOEDKEURING')
        decisions.append({"corrective_id":cid,"mandate_id":rec.get('mandate_id',''),"risk":rec.get('risk',''),"proposed_action":best.get('action',''),"proposal":best.get('description',''),"budget_change":float(best.get('cost_impact',0) or 0),"schedule_change_days":int(best.get('schedule_impact_days',0) or 0),"approval_level":prev.get('approval_level','BESTUUR' if float(best.get('cost_impact',0) or 0)==0 else 'ALV'),"status":status,"decision":decision,"rationale":prev.get('rationale',''),"approved_by":prev.get('approved_by',''),"approved_at":prev.get('approved_at',''),"created_at":prev.get('created_at',now),"updated_at":now,"mandate_amendment":prev.get('mandate_amendment',{})})
    approved=sum(str(x['decision']).upper() in {'GOEDGEKEURD','AKKOORD','APPROVED'} for x in decisions); pending=sum(str(x['status']).upper() not in {'AFGEROND','BESLOTEN','CLOSED'} for x in decisions)
    return {"corrective_decision_version":ENGINE_VERSION,"generated_at":now,"status":"GOEDKEURING VEREIST" if pending else "AFGEROND","decision_count":len(decisions),"approved_count":approved,"pending_count":pending,"decisions":decisions,"next_action":decisions[0]['proposal'] if pending and decisions else 'Geen correctief besluit vereist.'}

def approved_mandate_amendments(workflow:dict[str,Any])->list[dict[str,Any]]:
    result=[]
    for d in workflow.get('decisions',[]) or []:
        if str(d.get('decision','')).upper() not in {'GOEDGEKEURD','AKKOORD','APPROVED'}: continue
        result.append({"corrective_id":d.get('corrective_id',''),"mandate_id":d.get('mandate_id',''),"action":d.get('proposed_action',''),"budget_change":float(d.get('budget_change',0) or 0),"schedule_change_days":int(d.get('schedule_change_days',0) or 0),"rationale":d.get('rationale',''),"approved_by":d.get('approved_by',''),"approved_at":d.get('approved_at','')})
    return result
