"""Translate a locked strategy into measurable execution KPIs and monthly on-track status."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION='6.4.0'

def build_strategy_execution_scorecard(strategy:dict[str,Any], report:dict[str,Any])->dict[str,Any]:
    now=datetime.now(timezone.utc).isoformat(); lock=strategy.get('strategy_lock',{}) or {}
    if lock.get('status')!='VERGRENDELD':
        return {'strategy_execution_scorecard_version':ENGINE_VERSION,'generated_at':now,'status':'WACHT OP STRATEGIE','score':0,'kpis':[],'next_action':'Vergrendel eerst een door Bestuur/ALV goedgekeurd scenario.'}
    baseline=lock.get('baseline',{}) or {}; tower=report.get('governance_control_tower',{}) or {}; tk=tower.get('kpis',{}) or {}; forecast=report.get('mandate_forecast',{}) or {}; compliance=report.get('mandate_compliance',{}) or {}; effectiveness=report.get('amendment_effectiveness',{}) or {}; deviation=strategy.get('deviation',{}) or {}
    budget=float(tk.get('total_mandate_budget',0) or 0); reserve=float(tk.get('reserve',0) or 0); pressure=(budget/reserve*100) if reserve>0 else 0
    target_pressure=float(baseline.get('reserve_pressure_percent',0) or 0); current_risk=float(sum(int(x.get('risk_score',0) or 0) for x in (report.get('executive_risk_radar',{}) or {}).get('outlook',[]) or [])); target_risk=float(baseline.get('adjusted_12m_risk',0) or 0)
    kpis=[
      {'domain':'FINANCIEEL','kpi':'Reservedruk','target':target_pressure,'actual':round(pressure,1),'unit':'%','on_track':pressure<=target_pressure+5},
      {'domain':'RISICO','kpi':'12-maands risicodruk','target':target_risk,'actual':round(current_risk,1),'unit':'score','on_track':current_risk<=target_risk+5},
      {'domain':'COMPLIANCE','kpi':'Rode mandaten','target':0,'actual':int(compliance.get('red_count',0) or 0),'unit':'aantal','on_track':int(compliance.get('red_count',0) or 0)==0},
      {'domain':'UITVOERING','kpi':'Hoog-risico mandaten','target':0,'actual':int(forecast.get('high_risk_count',0) or 0),'unit':'aantal','on_track':int(forecast.get('high_risk_count',0) or 0)==0},
      {'domain':'GOVERNANCE','kpi':'Open amendment-effecten','target':0,'actual':int(effectiveness.get('open_count',0) or 0),'unit':'aantal','on_track':int(effectiveness.get('open_count',0) or 0)==0},
      {'domain':'STRATEGIE','kpi':'Strategische afwijking','target':0,'actual':int(deviation.get('score',0) or 0),'unit':'score','on_track':int(deviation.get('score',0) or 0)<20},
    ]
    achieved=sum(1 for x in kpis if x['on_track']); score=round(achieved/len(kpis)*100,1) if kpis else 0
    status='OP KOERS' if score>=85 else 'AANDACHT' if score>=60 else 'BUITEN KOERS'
    off=[x for x in kpis if not x['on_track']]
    return {'strategy_execution_scorecard_version':ENGINE_VERSION,'generated_at':now,'decision_id':lock.get('decision_id',''),'selected_scenario':lock.get('selected_scenario',''),'status':status,'score':score,'kpi_count':len(kpis),'on_track_count':achieved,'off_track_count':len(off),'kpis':kpis,'off_track_domains':[x['domain'] for x in off],'next_action':'Reguliere maandmonitoring voortzetten.' if not off else f"Stuur bij op {off[0]['domain']}: {off[0]['kpi']}."}
