"""Enterprise 13.3 Constitutional Governance Forecast & Time-to-Red Prediction."""
from __future__ import annotations
from math import ceil
from typing import Any
ENGINE_VERSION='13.3.0'

def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def _time_to_threshold(current:float,slope:float,threshold:float,direction:str)->int|None:
 if direction=='up':
  if current>=threshold:return 0
  if slope<=0:return None
  return max(0,ceil((threshold-current)/slope))
 if current<=threshold:return 0
 if slope>=0:return None
 return max(0,ceil((current-threshold)/abs(slope)))

def forecast_governance_time_to_red(radar:dict[str,Any], current:dict[str,Any], runs_per_year:float=12.0)->dict[str,Any]:
 trends=radar.get('trend_metrics',{}) or {}
 debt=_num(current.get('constitutional_debt_score',0)); health=_num(current.get('constitutional_health_score',100)); waivers=_num(current.get('active_waivers',0)); migrations=_num(current.get('open_migrations',0))
 debt_slope=_num(trends.get('debt_slope',0)); health_slope=_num(trends.get('health_slope',0)); waiver_slope=_num(trends.get('waiver_slope',0)); migration_slope=_num(trends.get('migration_slope',0)); assurance_slope=_num(trends.get('assurance_slope',0))
 targets={
  'debt_orange':_time_to_threshold(debt,debt_slope,40,'up'),'debt_red':_time_to_threshold(debt,debt_slope,70,'up'),
  'health_orange':_time_to_threshold(health,health_slope,70,'down'),'health_red':_time_to_threshold(health,health_slope,55,'down'),
  'waiver_pressure':_time_to_threshold(waivers,waiver_slope,3,'up'),'migration_pressure':_time_to_threshold(migrations,migration_slope,3,'up'),
  'assurance_escalation':0 if assurance_slope>0 and str(current.get('assurance_decision','BEHOUDEN')).upper()=='ROLLBACK' else (ceil(1/assurance_slope) if assurance_slope>0 else None)
 }
 candidates=[x for x in targets.values() if x is not None]
 nearest=min(candidates) if candidates else None
 months=None if nearest is None or runs_per_year<=0 else round(nearest*12/runs_per_year,1)
 alerts=[]
 for key,val in targets.items():
  if val is not None and val<=3: alerts.append({'priority':'KRITIEK' if val<=1 else 'HOOG','metric':key,'runs_to_threshold':val})
 if nearest is None: status='GEEN ROODPAD GEPROJECTEERD'
 elif nearest<=1: status='ROOD BINNEN 1 BESTUURSRUN'
 elif nearest<=3: status='ROOD/ORANJE BINNEN 3 RUNS'
 else: status='VERSLECHTERING GEPROJECTEERD'
 return {'constitutional_governance_forecast_time_to_red_version':ENGINE_VERSION,'status':status,'forecast_horizon_runs':nearest,'forecast_horizon_months':months,'runs_per_year':runs_per_year,'threshold_forecast_runs':targets,'forecast_alerts':alerts,'human_board_review_required':bool(alerts),'automatic_decision':False,'automatic_execution':False,'next_action':'Plan preventieve governance-interventie vóór de eerst geprojecteerde drempel.' if nearest is not None else 'Geen geprojecteerde kritieke drempel op basis van huidige trend.'}
