"""Enterprise 13.2 Constitutional Governance Trend & Early Drift Radar."""
from __future__ import annotations
from typing import Any
ENGINE_VERSION='13.2.0'

def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def _slope(values:list[float])->float:
 n=len(values)
 if n<2:return 0.0
 x=list(range(n)); xm=sum(x)/n; ym=sum(values)/n
 den=sum((i-xm)**2 for i in x)
 return 0.0 if den==0 else sum((i-xm)*(y-ym) for i,y in zip(x,values))/den

def analyze_governance_trend(pulses:list[dict[str,Any]], min_history:int=4)->dict[str,Any]:
 pulses=pulses or []
 if len(pulses)<min_history:
  return {'constitutional_governance_trend_drift_radar_version':ENGINE_VERSION,'status':'ONVOLDOENDE HISTORIE','early_drift_alerts':[],'human_board_review_required':False,'automatic_decision':False}
 debt=[_num(p.get('constitutional_debt_score',p.get('current_debt_score',0))) for p in pulses]
 waivers=[_num(p.get('active_waivers',p.get('current_active_waivers',0))) for p in pulses]
 migrations=[_num(p.get('open_migrations',p.get('current_open_migrations',0))) for p in pulses]
 health=[_num(p.get('constitutional_health_score',p.get('current_health_score',0))) for p in pulses]
 assurance_rank={'BEHOUDEN':0,'HERSTELLEN':1,'ROLLBACK':2}
 assurance=[assurance_rank.get(str(p.get('assurance_decision',p.get('current_assurance_decision','BEHOUDEN'))).upper(),0) for p in pulses]
 trends={'debt_slope':round(_slope(debt),2),'waiver_slope':round(_slope(waivers),2),'migration_slope':round(_slope(migrations),2),'health_slope':round(_slope(health),2),'assurance_slope':round(_slope(assurance),2)}
 alerts=[]
 if trends['debt_slope']>=3: alerts.append({'priority':'HOOG','type':'DEBT_DRIFT','message':'Constitutional Debt vertoont een structureel stijgende trend.'})
 if trends['waiver_slope']>=0.5: alerts.append({'priority':'HOOG','type':'WAIVER_DRIFT','message':'Actieve waivers nemen structureel toe.'})
 if trends['migration_slope']>=0.5: alerts.append({'priority':'HOOG','type':'MIGRATION_DRIFT','message':'Open migraties bouwen structureel op.'})
 if trends['health_slope']<=-2: alerts.append({'priority':'HOOG','type':'HEALTH_DRIFT','message':'Constitutional Health Score daalt structureel.'})
 if trends['assurance_slope']>0: alerts.append({'priority':'KRITIEK' if assurance[-1]>=2 else 'HOOG','type':'ASSURANCE_DRIFT','message':'Assurance beweegt structureel richting HERSTELLEN/ROLLBACK.'})
 drift_score=min(100.0,round(max(0,trends['debt_slope'])*8+max(0,trends['waiver_slope'])*15+max(0,trends['migration_slope'])*15+max(0,-trends['health_slope'])*8+max(0,trends['assurance_slope'])*20,1))
 level='ROOD' if drift_score>=70 else ('ORANJE' if drift_score>=40 else ('GEEL' if drift_score>0 else 'GROEN'))
 status='EARLY DRIFT KRITIEK' if level=='ROOD' else ('EARLY DRIFT GESIGNALEERD' if level in {'ORANJE','GEEL'} else 'TREND STABIEL')
 return {'constitutional_governance_trend_drift_radar_version':ENGINE_VERSION,'status':status,'drift_score':drift_score,'drift_level':level,'history_count':len(pulses),'trend_metrics':trends,'early_drift_alerts':alerts,'human_board_review_required':level in {'ORANJE','ROOD'},'automatic_decision':False,'automatic_execution':False,'next_action':'Start vroege governance-review op de oplopende trends.' if alerts else 'Geen vroege drift gedetecteerd; blijf monitoren.'}
