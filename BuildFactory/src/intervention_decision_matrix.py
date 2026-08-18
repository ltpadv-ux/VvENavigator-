"""Rank intervention options on affordability, risk, MJOP impact and strategic fit."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION='6.7.0'
DEFAULT_WEIGHTS={'cost':0.25,'risk':0.30,'affordability':0.20,'mjop':0.10,'strategic_fit':0.15}

def _norm(value:float,low:float,high:float,invert:bool=False)->float:
    if high<=low: return 100.0
    score=max(0.0,min(100.0,(value-low)/(high-low)*100.0))
    return 100.0-score if invert else score

def build_intervention_decision_matrix(impact:dict[str,Any], scorecard:dict[str,Any], weights:dict[str,float]|None=None)->dict[str,Any]:
    weights=weights or DEFAULT_WEIGHTS; rows=[]
    for sim in impact.get('simulations',[]) or []:
        opts=sim.get('options',[]) or []
        if not opts: continue
        costs=[float((o.get('horizons',{}).get('30',{}) or {}).get('lcc',0) or 0) for o in opts]
        monthlies=[float(o.get('monthly_delta',0) or 0) for o in opts]
        risks=[abs(float(o.get('risk_score_delta',0) or 0)) for o in opts]
        shifts=[abs(float(o.get('mjop_shift_months',0) or 0)) for o in opts]
        for o in opts:
            cost=float((o.get('horizons',{}).get('30',{}) or {}).get('lcc',0) or 0); monthly=abs(float(o.get('monthly_delta',0) or 0)); risk=abs(float(o.get('risk_score_delta',0) or 0)); shift=abs(float(o.get('mjop_shift_months',0) or 0))
            cost_score=_norm(cost,min(costs),max(costs),invert=True); affordability=_norm(monthly,min(monthlies),max(monthlies),invert=True); risk_score=_norm(risk,min(risks),max(risks)); mjop_score=_norm(shift,min(shifts),max(shifts),invert=True)
            strategic_fit=100.0 if scorecard.get('status')=='BUITEN KOERS' and risk>=12 else 85.0 if risk>=8 else 70.0
            total=round(cost_score*weights['cost']+risk_score*weights['risk']+affordability*weights['affordability']+mjop_score*weights['mjop']+strategic_fit*weights['strategic_fit'],1)
            rows.append({'intervention_id':sim.get('intervention_id',''),'domain':sim.get('domain',''),'kpi':sim.get('kpi',''),'option':o.get('option',''),'decision_authority':sim.get('decision_authority','Bestuur'),'scores':{'cost':round(cost_score,1),'risk':round(risk_score,1),'affordability':round(affordability,1),'mjop':round(mjop_score,1),'strategic_fit':round(strategic_fit,1)},'weighted_score':total,'impact':o})
    rows=sorted(rows,key=lambda x:(-x['weighted_score'],x['impact'].get('monthly_delta',0),(x['impact'].get('horizons',{}).get('30',{}) or {}).get('lcc',0)))
    for i,row in enumerate(rows,1): row['rank']=i
    preferred=rows[0] if rows else {}
    return {'intervention_decision_matrix_version':ENGINE_VERSION,'generated_at':datetime.now(timezone.utc).isoformat(),'weights':weights,'option_count':len(rows),'preferred_option':preferred.get('option',''),'preferred_intervention_id':preferred.get('intervention_id',''),'preferred_score':preferred.get('weighted_score',0),'decision_authority':preferred.get('decision_authority',''),'ranking':rows,'human_decision_required':bool(rows),'board_advice':f"Voorkeursvariant: {preferred.get('option','geen')} (score {preferred.get('weighted_score',0)})." if preferred else 'Geen interventievarianten beschikbaar.','next_action':'Leg de voorkeursvariant en alternatieven ter besluitvorming voor aan Bestuur/ALV.' if preferred else 'Geen actie.'}
