"""Enterprise 10.1 Executive Command Center Live KPI & Decision Pulse."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
ENGINE_VERSION='10.1.0'
TRACKED_KPIS=('health_governance_score','financial_health','mjop_health','risk_score','treasury_score','audit_assurance','governance_maturity','best_36m_score','downside_36m_score')

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _trend(delta:float, reverse:bool=False)->str:
    if abs(delta)<0.1:return '→'
    good=delta<0 if reverse else delta>0
    return '↑' if good else '↓'

def build_executive_decision_pulse(current:dict[str,Any], previous:dict[str,Any]|None=None, run_at:str|None=None)->dict[str,Any]:
    previous=previous or {}; now_summary=current.get('executive_summary',{}) or {}; prev_summary=(previous.get('executive_summary',{}) or {})
    changes=[]
    for key in TRACKED_KPIS:
        cur=_num(now_summary.get(key)); prev=_num(prev_summary.get(key)); delta=round(cur-prev,2)
        changes.append({'kpi':key,'current':cur,'previous':prev,'delta':delta,'trend':_trend(delta,reverse=(key=='risk_score'))})
    current_actions={str(x.get('recommendation_id') or x.get('topic')):x for x in current.get('top_board_actions',[]) or []}
    previous_actions={str(x.get('recommendation_id') or x.get('topic')):x for x in previous.get('top_board_actions',[]) or []}
    new_actions=[x for k,x in current_actions.items() if k not in previous_actions]
    closed_actions=[x for k,x in previous_actions.items() if k not in current_actions]
    changed_status=str(current.get('board_status',''))!=str(previous.get('board_status','')) if previous else False
    material=[x for x in changes if abs(float(x['delta']))>=2]
    pulse_status='KRITIEKE WIJZIGING' if str(current.get('board_status','')).upper()=='DIRECT BESLUIT VEREIST' and (new_actions or changed_status) else ('WIJZIGINGEN' if material or new_actions or closed_actions or changed_status else 'STABIEL')
    return {'executive_decision_pulse_version':ENGINE_VERSION,'run_at':run_at or datetime.now(timezone.utc).isoformat(),'pulse_status':pulse_status,'board_status':current.get('board_status','ONBEKEND'),'previous_board_status':previous.get('board_status','ONBEKEND') if previous else 'GEEN VORIGE RUN','board_status_changed':changed_status,'kpi_changes':changes,'material_kpi_changes':material,'new_board_actions':new_actions,'closed_board_actions':closed_actions,'new_action_count':len(new_actions),'closed_action_count':len(closed_actions),'critical_action_count':int(current.get('critical_action_count',0) or 0),'human_decision_required':True,'automatic_decision':False,'automatic_execution':False,'next_action':'Beoordeel eerst nieuwe kritieke acties en materiële KPI-verslechteringen.' if pulse_status!='STABIEL' else 'Geen materiële wijzigingen; vervolg reguliere monitoring.'}
