"""Build an auditable treasury decision lineage from signal to closure."""
from __future__ import annotations
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

ENGINE_VERSION='8.5.0'

def _hash(payload:str)->str:
    return sha256(payload.encode('utf-8')).hexdigest()

def build_treasury_audit_lineage(report:dict[str,Any])->dict[str,Any]:
    now=datetime.now(timezone.utc).isoformat()
    calendar=report.get('treasury_early_warning_calendar',{}) or {}
    board=report.get('treasury_decision_board_pack',{}) or {}
    accountability=report.get('treasury_accountability_register',{}) or {}
    effectiveness=report.get('treasury_decision_effectiveness',{}) or {}

    actions_by_agenda={x.get('agenda_id'):x for x in accountability.get('actions',[]) or []}
    closures_by_action={x.get('action_id'):x for x in effectiveness.get('closures',[]) or []}
    signals={
        f"{x.get('month','')}|{x.get('category','')}|{x.get('title','')}":x
        for x in calendar.get('actions',[]) or []
    }
    chains=[]
    for item in board.get('agenda_items',[]) or []:
        key=f"{item.get('month','')}|{item.get('category','')}|{item.get('title','')}"
        signal=signals.get(key,{})
        action=actions_by_agenda.get(item.get('agenda_id'),{})
        closure=closures_by_action.get(action.get('action_id'),{}) if action else {}
        nodes=[
            {'type':'SIGNAL','id':_hash(key)[:12].upper(),'status':signal.get('severity','ONBEKEND'),'evidence':signal.get('detail','')},
            {'type':'DECISION','id':item.get('agenda_id',''),'status':item.get('decision','NOG TE BESLUITEN'),'evidence':item.get('rationale','')},
        ]
        if action:
            nodes.append({'type':'EXECUTION','id':action.get('action_id',''),'status':action.get('status',''),'evidence':action.get('evidence',[])})
        if closure:
            nodes.append({'type':'EFFECT','id':closure.get('action_id',''),'status':closure.get('status',''),'evidence':closure.get('checks',[])})
        chain_payload='|'.join(str(n.get('id',''))+':'+str(n.get('status','')) for n in nodes)
        chain_hash=_hash(chain_payload)
        complete=bool(signal) and bool(item.get('agenda_id')) and (str(item.get('decision','')).upper() not in {'GOEDGEKEURD','AKKOORD','APPROVED'} or bool(action))
        if action and action.get('status')=='AFGEROND':
            complete=complete and bool(closure)
        chains.append({
            'lineage_id':'TRLIN-'+chain_hash[:10].upper(),
            'agenda_id':item.get('agenda_id',''),
            'title':item.get('title',''),
            'category':item.get('category',''),
            'month':item.get('month',''),
            'nodes':nodes,
            'chain_hash':chain_hash,
            'complete':complete,
            'closure_status':closure.get('closure_status','OPEN' if action else 'NIET VAN TOEPASSING'),
        })
    incomplete=sum(not x['complete'] for x in chains)
    closed=sum(x['closure_status']=='GESLOTEN' for x in chains)
    status='GEEN AUDITKETENS' if not chains else ('AUDIT TRAIL COMPLEET' if incomplete==0 else 'AUDIT GAP GEVONDEN')
    return {
        'treasury_audit_lineage_version':ENGINE_VERSION,
        'generated_at':now,
        'status':status,
        'chain_count':len(chains),
        'complete_chain_count':len(chains)-incomplete,
        'incomplete_chain_count':incomplete,
        'closed_chain_count':closed,
        'chains':chains,
        'tamper_evident_hashing':True,
        'human_governance_preserved':True,
        'automatic_decision':False,
        'next_action':'Audit trail is compleet; exporteer voor Bestuur/ALV/accountant.' if status=='AUDIT TRAIL COMPLEET' else ('Vul ontbrekende signalen, besluiten, uitvoeringsbewijzen of effectmetingen aan.' if chains else 'Geen treasurybesluiten om te auditen.')
    }
