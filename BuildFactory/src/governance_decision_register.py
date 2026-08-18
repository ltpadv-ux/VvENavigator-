"""Governance dashboard and auditable human decision register."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import hashlib, json

ENGINE_VERSION="5.1.0"

def _decision_id(gate: dict[str,Any]) -> str:
    raw=f"{gate.get('gate','')}|{gate.get('owner','')}|{gate.get('reason','')}"
    return "DEC-"+hashlib.sha256(raw.encode()).hexdigest()[:10].upper()

def build_decision_register(autonomous: dict[str,Any], existing: dict[str,Any]|None=None) -> dict[str,Any]:
    old={x.get('id'):x for x in (existing or {}).get('decisions',[]) or []}; now=datetime.now(timezone.utc).isoformat(); decisions=[]
    for gate in autonomous.get('human_decision_gates',[]) or []:
        did=_decision_id(gate); prev=old.get(did,{})
        decisions.append({"id":did,"gate":gate.get('gate',''),"owner":prev.get('owner',gate.get('owner','Bestuur / Beheerder')),"reason":gate.get('reason',''),"status":prev.get('status','OPEN'),"decision":prev.get('decision','NOG TE BESLUITEN'),"rationale":prev.get('rationale',''),"created_at":prev.get('created_at',now),"updated_at":now})
    open_count=sum(str(x['status']).upper() not in {'GEREED','CLOSED','BESLOTEN'} for x in decisions)
    dashboard={"governance_status":autonomous.get('cycle_status','ONBEKEND'),"release_status":autonomous.get('release_status','ONBEKEND'),"sla_compliant":bool(autonomous.get('sla_compliant',False)),"open_decisions":open_count,"total_decisions":len(decisions),"next_action":autonomous.get('next_action','')}
    return {"decision_register_version":ENGINE_VERSION,"generated_at":now,"dashboard":dashboard,"decisions":decisions,"audit_hash":hashlib.sha256(json.dumps(decisions,sort_keys=True,ensure_ascii=False).encode()).hexdigest()}
