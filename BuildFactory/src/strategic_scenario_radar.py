"""Compare Basis, Duurzaam and Versneld scenarios on 12-month governance robustness."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION="6.2.0"
DEFAULT_SCENARIOS={
    "Basis":{"risk_factor":1.0,"cost_factor":1.0,"schedule_factor":1.0},
    "Duurzaam":{"risk_factor":0.85,"cost_factor":1.08,"schedule_factor":1.05},
    "Versneld":{"risk_factor":0.9,"cost_factor":1.15,"schedule_factor":0.8},
}

def build_strategic_scenario_radar(radar:dict[str,Any], tower:dict[str,Any], scenarios:dict[str,Any]|None=None)->dict[str,Any]:
    scenarios=scenarios or DEFAULT_SCENARIOS
    base_risk=sum(int(x.get('risk_score',0) or 0) for x in radar.get('outlook',[]) or [])
    reserve=float((tower.get('kpis',{}) or {}).get('reserve',0) or 0)
    mandate_budget=float((tower.get('kpis',{}) or {}).get('total_mandate_budget',0) or 0)
    results=[]
    for name,cfg in scenarios.items():
        risk_factor=float(cfg.get('risk_factor',1.0)); cost_factor=float(cfg.get('cost_factor',1.0)); schedule_factor=float(cfg.get('schedule_factor',1.0))
        adjusted_risk=round(base_risk*risk_factor,2); adjusted_budget=round(mandate_budget*cost_factor,2)
        reserve_pressure=round((adjusted_budget/reserve)*100,1) if reserve>0 else 0.0
        robustness=max(0.0,100.0-adjusted_risk-(max(0,reserve_pressure-100)*0.5)-max(0,(schedule_factor-1)*20))
        status='ROBUUST' if robustness>=80 else 'AANDACHT' if robustness>=60 else 'KWETSBAAR'
        results.append({"scenario":name,"robustness_score":round(robustness,1),"status":status,"adjusted_12m_risk":adjusted_risk,"adjusted_mandate_budget":adjusted_budget,"reserve_pressure_percent":reserve_pressure,"schedule_factor":schedule_factor,"assumptions":cfg})
    results=sorted(results,key=lambda x:(-x['robustness_score'],x['adjusted_mandate_budget']))
    preferred=results[0] if results else {}
    return {"strategic_scenario_radar_version":ENGINE_VERSION,"generated_at":datetime.now(timezone.utc).isoformat(),"scenario_count":len(results),"preferred_scenario":preferred.get('scenario',''),"preferred_robustness_score":preferred.get('robustness_score',0),"scenarios":results,"board_advice":f"Voorkeur: {preferred.get('scenario','geen')} met robuustheidsscore {preferred.get('robustness_score',0)}." if preferred else 'Geen scenariovergelijking beschikbaar.',"next_action":"Bespreek voorkeurscenario en aannames in bestuur/ALV." if preferred else 'Geen actie.'}
