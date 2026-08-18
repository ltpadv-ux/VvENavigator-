"""Integrated Governance Control Tower: one executive view across governance, ALV, mandates and finance."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION="6.0.0"

def build_control_tower(report:dict[str,Any])->dict[str,Any]:
    auto=report.get('autonomous_governance',{}) or {}; reg=report.get('governance_decision_register',{}) or {}; alv=report.get('alv_decision_workflow',{}) or {}; mandates=report.get('alv_execution_mandates',{}) or {}; comp=report.get('mandate_compliance',{}) or {}; forecast=report.get('mandate_forecast',{}) or {}; corrective=report.get('corrective_decision_workflow',{}) or {}; effectiveness=report.get('amendment_effectiveness',{}) or {}; sla=report.get('reliability_sla',{}) or {}
    metrics=(((report.get('release',{}) or {}).get('executive_cockpit',{}) or {}).get('key_metrics',{}) or {})
    red=int(comp.get('red_count',0) or 0); high=int(forecast.get('high_risk_count',0) or 0); pending=int(corrective.get('pending_count',0) or 0); open_decisions=int((reg.get('dashboard',{}) or {}).get('open_decisions',0) or 0); open_effect=int(effectiveness.get('open_count',0) or 0)
    score=max(0,100-red*30-high*20-pending*10-open_decisions*10-open_effect*10-(0 if sla.get('compliant',False) else 20))
    status='GROEN' if score>=80 else 'ORANJE' if score>=50 else 'ROOD'
    priorities=[]
    if red: priorities.append('Los geblokkeerde mandaten en bestuurlijke escalaties op.')
    if high: priorities.append('Behandel mandaten met hoog forecast-risico.')
    if pending: priorities.append('Neem openstaande correctieve besluiten.')
    if open_decisions: priorities.append('Rond open governancebesluiten af.')
    if open_effect: priorities.append('Verzamel effectbewijs voor open amendments.')
    if not sla.get('compliant',False): priorities.append('Herstel releasebetrouwbaarheid tot SLA-niveau.')
    return {"control_tower_version":ENGINE_VERSION,"generated_at":datetime.now(timezone.utc).isoformat(),"overall_status":status,"governance_score":score,"kpis":{"autonomous_status":auto.get('cycle_status','ONBEKEND'),"sla_compliant":bool(sla.get('compliant',False)),"open_governance_decisions":open_decisions,"alv_items":int(alv.get('item_count',0) or 0),"open_mandates":int(mandates.get('open_count',0) or 0),"blocked_mandates":red,"high_risk_mandates":high,"pending_corrective_decisions":pending,"open_amendment_effects":open_effect,"total_mandate_budget":float(mandates.get('total_budget',0) or 0),"total_mandate_spent":float(mandates.get('total_spent',0) or 0),"monthly_per_apartment":float(metrics.get('monthly_per_apartment',0) or 0),"reserve":float(metrics.get('reserve',0) or 0)},"priority_actions":priorities,"next_action":priorities[0] if priorities else 'Control Tower is groen; reguliere monitoring voortzetten.'}
