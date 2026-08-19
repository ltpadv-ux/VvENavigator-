"""Translate approved treasury board-pack decisions into accountable execution actions."""
from __future__ import annotations
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

ENGINE_VERSION='8.3.0'
APPROVED={'GOEDGEKEURD','AKKOORD','APPROVED'}

def _id(prefix:str,*parts:Any)->str:
    raw='|'.join(str(x) for x in parts).encode()
    return f"{prefix}-{sha256(raw).hexdigest()[:10].upper()}"

def build_treasury_accountability_register(board_pack:dict[str,Any], existing:dict[str,Any]|None=None)->dict[str,Any]:
    now=datetime.now(timezone.utc).isoformat(); existing=existing or {}; prev={x.get('action_id'):x for x in existing.get('actions',[]) or []}; actions=[]
    for item in board_pack.get('agenda_items',[]) or []:
        if str(item.get('decision','')).upper() not in APPROVED:
            continue
        action_id=_id('TRACT',item.get('agenda_id',''),item.get('title',''))
        old=prev.get(action_id,{})
        progress=float(old.get('progress_percent',0) or 0); spent=float(old.get('spent',0) or 0); budget=float(old.get('budget',0) or 0)
        owner=str(old.get('owner') or item.get('owner') or 'Bestuur / beheerder'); deadline=str(old.get('deadline') or item.get('deadline') or item.get('month',''))
        evidence=old.get('evidence',[]) or []; completed=progress>=100 and bool(evidence)
        status='AFGEROND' if completed else ('IN UITVOERING' if progress>0 else 'OPEN')
        actions.append({'action_id':action_id,'agenda_id':item.get('agenda_id',''),'title':item.get('title',''),'category':item.get('category',''),'severity':item.get('severity',''),'decision_authority':item.get('decision_authority',''),'owner':owner,'deadline':deadline,'budget':budget,'spent':spent,'budget_remaining':round(budget-spent,2) if budget else None,'progress_percent':progress,'evidence':evidence,'status':status,'approved_by':item.get('approved_by',''),'approved_at':item.get('approved_at',''),'updated_at':now})
    open_count=sum(a['status']!='AFGEROND' for a in actions); overdue=sum(a['status']!='AFGEROND' and bool(a['deadline']) and a['deadline'] < now[:7] for a in actions); over_budget=sum(a['budget']>0 and a['spent']>a['budget'] for a in actions)
    accountability_score=100-max(0,open_count*8+overdue*20+over_budget*20); accountability_score=max(0,accountability_score)
    status='GEEN GOEDGEKEURDE ACTIES' if not actions else ('ESCALATIE VEREIST' if overdue or over_budget else ('UITVOERING LOPEND' if open_count else 'VOLLEDIG UITGEVOERD'))
    return {'treasury_accountability_version':ENGINE_VERSION,'generated_at':now,'status':status,'accountability_score':accountability_score,'action_count':len(actions),'open_count':open_count,'overdue_count':overdue,'over_budget_count':over_budget,'actions':actions,'automatic_execution':False,'human_accountability_required':True,'next_action':'Geen goedgekeurde treasuryacties.' if not actions else ('Escalatie naar Bestuur/ALV voor achterstallige of budgetoverschrijdende acties.' if status=='ESCALATIE VEREIST' else ('Werk open acties bij met voortgang, besteding en bewijs.' if open_count else 'Alle goedgekeurde treasurybesluiten zijn aantoonbaar uitgevoerd.'))}
