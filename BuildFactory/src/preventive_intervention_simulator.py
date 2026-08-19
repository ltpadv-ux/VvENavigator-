"""Enterprise 10.4 Preventive Intervention Simulator & Impact Preview."""
from __future__ import annotations
from typing import Any
ENGINE_VERSION='10.4.0'

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def simulate_preventive_interventions(trend_radar:dict[str,Any], command_center:dict[str,Any], horizon_months:int=12)->dict[str,Any]:
    alerts=[a for a in trend_radar.get('early_intervention_alerts',[]) or [] if str(a.get('severity','')).upper() in {'GEEL','ORANJE','ROOD'}]
    if not alerts:
        return {'preventive_intervention_simulator_version':ENGINE_VERSION,'status':'GEEN PREVENTIEVE INTERVENTIE NODIG','scenarios':[],'recommended_scenario':{},'automatic_intervention':False}
    summary=command_center.get('executive_summary',{}) or {}
    base_health=_num(summary.get('health_governance_score'))
    base_risk=_num(summary.get('risk_score'))
    severity_weight={'GEEL':1.0,'ORANJE':1.8,'ROOD':2.8}
    pressure=sum(severity_weight.get(str(a.get('severity','')).upper(),1.0) for a in alerts)
    do_nothing_health=max(0.0,round(base_health-pressure*2.5,1))
    do_nothing_risk=min(100.0,round(base_risk+pressure*3.0,1))
    delayed_cost=round(pressure*25000,2)
    early_cost=round(pressure*9000,2)
    early_health=min(100.0,round(base_health+pressure*0.8,1))
    early_risk=max(0.0,round(base_risk-pressure*1.8,1))
    avoided=max(0.0,round(delayed_cost-early_cost,2))
    scenarios=[
      {'scenario':'NIETS DOEN','horizon_months':horizon_months,'projected_health_score':do_nothing_health,'projected_risk_score':do_nothing_risk,'estimated_cost':delayed_cost,'avoided_recovery_cost':0.0,'board_action':'Geen preventieve actie.'},
      {'scenario':'VROEG INGRIJPEN','horizon_months':horizon_months,'projected_health_score':early_health,'projected_risk_score':early_risk,'estimated_cost':early_cost,'avoided_recovery_cost':avoided,'board_action':'Start preventieve interventie op de hoogste trendbreukprioriteiten.'}
    ]
    recommended=max(scenarios,key=lambda x:(x['projected_health_score']-x['projected_risk_score']*0.25-x['estimated_cost']/100000))
    return {'preventive_intervention_simulator_version':ENGINE_VERSION,'status':'IMPACT PREVIEW BESCHIKBAAR','trigger_alert_count':len(alerts),'scenarios':scenarios,'recommended_scenario':recommended,'health_score_uplift_vs_no_action':round(early_health-do_nothing_health,1),'risk_reduction_vs_no_action':round(do_nothing_risk-early_risk,1),'avoided_recovery_cost':avoided,'human_decision_required':True,'automatic_intervention':False,'automatic_budget_commitment':False,'next_action':'Laat Bestuur/ALV vroeg ingrijpen versus niets doen beoordelen op effect, risico en kosten.'}
