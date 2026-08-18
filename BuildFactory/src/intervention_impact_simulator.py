"""Simulate intervention proposals across reserve, contribution, MJOP, risk and NPV/LCC horizons."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

ENGINE_VERSION='6.6.0'
HORIZONS=(10,20,30)

def _npv(cost:float,years:int,discount:float)->float:
    return round(sum(cost/((1+discount)**y) for y in range(1,years+1)),2)

def simulate_intervention_impacts(interventions:dict[str,Any], report:dict[str,Any], discount_rate:float=0.03)->dict[str,Any]:
    now=datetime.now(timezone.utc).isoformat(); proposals=interventions.get('proposals',[]) or []
    tower=(report.get('governance_control_tower',{}) or {}).get('kpis',{}) or {}; reserve=float(tower.get('reserve',0) or 0); apartments=int((((report.get('release',{}) or {}).get('dataset',{}) or {}).get('apartments',0) or 0) or 34); monthly=float(tower.get('monthly_per_apartment',0) or 0)
    simulations=[]
    for i,p in enumerate(proposals,1):
        domain=p.get('domain',''); exposure=p.get('estimated_financial_exposure',0)
        exposure=float(exposure) if isinstance(exposure,(int,float)) else 0.0
        options=[]
        for opt in p.get('options',[]) or []:
            text=str(opt); reserve_delta=0.0; monthly_delta=0.0; risk_delta=-10.0; mjop_shift=0
            if 'Faseer' in text or 'Herplan' in text or 'deadline' in text.lower(): reserve_delta=exposure*0.5; mjop_shift=12; risk_delta=-7
            elif 'bijdrage' in text.lower() or 'financiering' in text.lower(): monthly_delta=(exposure/apartments/12) if apartments else 0; reserve_delta=exposure; risk_delta=-8
            elif 'Versnel' in text or 'Mitigeer' in text: reserve_delta=-exposure*0.25; mjop_shift=-6; risk_delta=-12
            elif 'Blokkeer' in text or 'Herstel' in text: risk_delta=-15
            projected_reserve=reserve+reserve_delta
            projected_monthly=max(0,monthly+monthly_delta)
            annual_cost=max(0,monthly_delta*apartments*12)
            horizons={str(y):{'npv':_npv(annual_cost,y,discount_rate),'lcc':round(annual_cost*y+max(0,-reserve_delta),2)} for y in HORIZONS}
            options.append({'option':text,'projected_reserve':round(projected_reserve,2),'monthly_contribution_per_apartment':round(projected_monthly,2),'monthly_delta':round(monthly_delta,2),'mjop_shift_months':mjop_shift,'risk_score_delta':risk_delta,'horizons':horizons})
        simulations.append({'intervention_id':f'INT-{i:03d}','domain':domain,'kpi':p.get('kpi',''),'decision_authority':p.get('decision_authority','Bestuur'),'options':options})
    return {'intervention_impact_simulator_version':ENGINE_VERSION,'generated_at':now,'discount_rate':discount_rate,'horizons_years':list(HORIZONS),'simulation_count':len(simulations),'simulations':simulations,'human_decision_required':bool(simulations),'next_action':'Geen interventies om door te rekenen.' if not simulations else 'Vergelijk impactopties en leg voorkeursmaatregel ter besluitvorming voor.'}
