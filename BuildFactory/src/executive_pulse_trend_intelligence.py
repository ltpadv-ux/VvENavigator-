"""Enterprise 10.2 Executive Decision Pulse History & Trend Intelligence."""
from __future__ import annotations
from statistics import mean
from typing import Any
ENGINE_VERSION='10.2.0'
TRACKED=('health_governance_score','financial_health','mjop_health','risk_score','treasury_score','audit_assurance','governance_maturity','best_36m_score','downside_36m_score')

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _classify(values:list[float], reverse:bool=False)->dict[str,Any]:
    if len(values)<2:return {'trend':'ONVOLDOENDE DATA','slope':0.0,'deviation':0.0}
    deltas=[values[i]-values[i-1] for i in range(1,len(values))]
    slope=round(mean(deltas),2)
    recent=round(values[-1]-values[-2],2)
    long=round(values[-1]-values[0],2)
    effective=-slope if reverse else slope
    if abs(slope)<0.5: trend='STABIEL'
    elif effective>0: trend='VERBETERT'
    else: trend='VERSLECHTERT'
    expected=values[-2]+slope
    deviation=round(values[-1]-expected,2)
    if reverse: deviation=-deviation
    return {'trend':trend,'slope':slope,'recent_delta':recent,'long_term_delta':long,'deviation':deviation,'deviation_flag':abs(deviation)>=3}

def build_pulse_trend_intelligence(current_pulse:dict[str,Any], history:dict[str,Any]|None=None, max_history:int=24)->dict[str,Any]:
    history=history or {}; runs=list(history.get('runs',[]) or [])
    snapshot={'run_at':current_pulse.get('run_at',''),'board_status':current_pulse.get('board_status',''),'pulse_status':current_pulse.get('pulse_status',''),'kpis':{x.get('kpi'):x.get('current',0) for x in current_pulse.get('kpi_changes',[]) or []},'new_action_count':current_pulse.get('new_action_count',0),'closed_action_count':current_pulse.get('closed_action_count',0),'critical_action_count':current_pulse.get('critical_action_count',0)}
    if not runs or runs[-1].get('run_at')!=snapshot['run_at']: runs.append(snapshot)
    runs=runs[-max(2,max_history):]
    domains={}
    for key in TRACKED:
        vals=[_num(r.get('kpis',{}).get(key)) for r in runs if key in (r.get('kpis',{}) or {})]
        domains[key]=_classify(vals,reverse=(key=='risk_score'))
    deteriorating=[k for k,v in domains.items() if v.get('trend')=='VERSLECHTERT']
    deviations=[k for k,v in domains.items() if v.get('deviation_flag')]
    status='TRENDWAARSCHUWING' if deteriorating or deviations else ('TREND OPBOUWEN' if len(runs)<3 else 'STABIELE TREND')
    return {'executive_pulse_trend_intelligence_version':ENGINE_VERSION,'status':status,'history_count':len(runs),'runs':runs,'domain_trends':domains,'deteriorating_domains':deteriorating,'deviation_domains':deviations,'board_status_history':[r.get('board_status','') for r in runs],'human_decision_required':True,'automatic_intervention':False,'next_action':'Beoordeel verslechterende of afwijkende domeinen en koppel zo nodig een bestuurlijke actie.' if status=='TRENDWAARSCHUWING' else 'Blijf trendhistorie opbouwen en monitor structurele ontwikkeling.'}
