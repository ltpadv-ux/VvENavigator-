"""Evaluate whether mandate amendments demonstrably reduced execution risk."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION="5.9.0"
RISK_SCORE={"LAAG":0,"MIDDEL":1,"HOOG":2}

def evaluate_amendment_effectiveness(amendment_result:dict[str,Any], before_compliance:dict[str,Any], before_forecast:dict[str,Any], after_compliance:dict[str,Any], after_forecast:dict[str,Any])->dict[str,Any]:
    before_f={str(x.get('mandate_id','')):x for x in before_forecast.get('forecasts',[]) or []}; after_f={str(x.get('mandate_id','')):x for x in after_forecast.get('forecasts',[]) or []}
    after_c={str(x.get('mandate_id','')):x for x in after_compliance.get('mandates',[]) or []}; evaluations=[]
    for a in amendment_result.get('applied',[]) or []:
        mid=str(a.get('mandate_id','')); bf=before_f.get(mid,{}); af=after_f.get(mid,{}); ac=after_c.get(mid,{})
        before_risk=str(bf.get('risk','LAAG')).upper(); after_risk=str(af.get('risk','LAAG')).upper(); compliance_status=str(ac.get('compliance_status','GROEN')).upper()
        risk_reduced=RISK_SCORE.get(after_risk,2)<RISK_SCORE.get(before_risk,2) or after_risk=='LAAG'
        within_budget=float(ac.get('spent_amount',0) or 0)<=float(ac.get('budget',0) or 0) if float(ac.get('budget',0) or 0)>0 else True
        no_red=compliance_status!='ROOD'; closed=risk_reduced and within_budget and no_red and after_risk=='LAAG'
        evaluations.append({"corrective_id":a.get('corrective_id',''),"mandate_id":mid,"before_risk":before_risk,"after_risk":after_risk,"risk_reduced":risk_reduced,"within_budget":within_budget,"compliance_status":compliance_status,"closure_status":"GESLOTEN" if closed else "OPEN","evidence":{"before_projected_final_cost":bf.get('projected_final_cost',0),"after_projected_final_cost":af.get('projected_final_cost',0),"after_budget":ac.get('budget',0),"after_spent":ac.get('spent_amount',0)}})
    closed_count=sum(x['closure_status']=='GESLOTEN' for x in evaluations); open_count=len(evaluations)-closed_count
    return {"amendment_effectiveness_version":ENGINE_VERSION,"generated_at":datetime.now(timezone.utc).isoformat(),"status":"EFFECT BEWEZEN" if evaluations and open_count==0 else "NADER BEWIJS NODIG" if evaluations else "GEEN AMENDEMENTEN","evaluation_count":len(evaluations),"closed_count":closed_count,"open_count":open_count,"evaluations":evaluations,"next_action":"Sluit de bewezen effectieve mandaatwijzigingen." if closed_count else "Blijf uitvoeren en monitor risico, budget en planning."}
