"""Executive Risk Radar & 12-Month Outlook for the Governance Control Tower."""
from __future__ import annotations
from datetime import date, datetime, timezone
from typing import Any

ENGINE_VERSION="6.1.0"
SEVERITY={"LAAG":1,"MIDDEL":2,"HOOG":3,"ROOD":4}

def build_risk_radar(report:dict[str,Any], months:int=12)->dict[str,Any]:
    tower=report.get('governance_control_tower',{}) or {}; mandates=report.get('alv_execution_mandates',{}) or {}; forecast=report.get('mandate_forecast',{}) or {}; compliance=report.get('mandate_compliance',{}) or {}; reg=report.get('governance_decision_register',{}) or {}; alv=report.get('alv_decision_workflow',{}) or {}; release=report.get('release',{}) or {}
    risks=[]
    for f in forecast.get('forecasts',[]) or []:
        risk=str(f.get('risk','LAAG')).upper()
        if risk in {'MIDDEL','HOOG'}:
            risks.append({"domain":"MANDAAT","subject":f.get('mandate_id',''),"severity":risk,"horizon_month":1 if risk=='HOOG' else 3,"signal":'; '.join(f.get('reasons',[]) or []) or 'Forecast-risico','action':'Beoordeel correctieve maatregel en mandaatplanning.'})
    for finding in compliance.get('findings',[]) or []:
        sev='HOOG' if str(finding.get('severity','')).upper()=='ROOD' else 'MIDDEL'
        risks.append({"domain":"COMPLIANCE","subject":finding.get('mandate_id',''),"severity":sev,"horizon_month":0,"signal":'; '.join(finding.get('issues',[]) or []),'action':finding.get('escalation','Beheeractie')})
    open_decisions=int((reg.get('dashboard',{}) or {}).get('open_decisions',0) or 0)
    if open_decisions:
        risks.append({"domain":"GOVERNANCE","subject":"Decision Register","severity":"MIDDEL","horizon_month":2,"signal":f'{open_decisions} open governancebesluit(en)','action':'Agendeer en rond besluiten tijdig af.'})
    if int(alv.get('ready_for_alv',0) or 0)>0:
        risks.append({"domain":"ALV","subject":"ALV Decision Workflow","severity":"MIDDEL","horizon_month":3,"signal":f"{int(alv.get('ready_for_alv',0) or 0)} voorstel(len) gereed voor ALV","action":"Plan besluitvorming en financiële toelichting."})
    metrics=((release.get('executive_cockpit',{}) or {}).get('key_metrics',{}) or {}); reserve=float(metrics.get('reserve',0) or 0); total_budget=float(mandates.get('total_budget',0) or 0); spent=float(mandates.get('total_spent',0) or 0)
    if total_budget>0 and reserve>0 and total_budget>reserve:
        risks.append({"domain":"FINANCIEEL","subject":"Reserve versus mandaten","severity":"HOOG","horizon_month":6,"signal":f'Mandaatbudget EUR {total_budget:.0f} > reserve EUR {reserve:.0f}',"action":"Herijk financiering, fasering en bijdrageontwikkeling.'"})
    risks=sorted(risks,key=lambda x:(-SEVERITY.get(x['severity'],0),x['horizon_month']))
    months_view=[]
    for m in range(1,months+1):
        bucket=[r for r in risks if int(r.get('horizon_month',months+1))<=m]
        score=sum(SEVERITY.get(r['severity'],0) for r in bucket)
        months_view.append({"month":m,"risk_score":score,"risk_count":len(bucket),"status":"ROOD" if score>=8 else "ORANJE" if score>=4 else "GROEN"})
    return {"executive_risk_radar_version":ENGINE_VERSION,"generated_at":datetime.now(timezone.utc).isoformat(),"outlook_months":months,"overall_control_tower_status":tower.get('overall_status','ONBEKEND'),"risk_count":len(risks),"high_risk_count":sum(r['severity']=='HOOG' for r in risks),"medium_risk_count":sum(r['severity']=='MIDDEL' for r in risks),"risks":risks,"outlook":months_view,"next_action":risks[0]['action'] if risks else 'Geen verhoogde risico’s in de 12-maands horizon.'}
