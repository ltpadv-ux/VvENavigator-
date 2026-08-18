"""Allocate scarce portfolio capital across VvEs using urgency, risk, affordability, LCC and sustainability."""
from __future__ import annotations
from typing import Any

ENGINE_VERSION='7.2.0'
DEFAULT_WEIGHTS={'urgency':0.25,'risk':0.25,'affordability':0.15,'lcc':0.20,'sustainability':0.15}

def _n(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _norm(value:float, values:list[float], higher_better:bool=True)->float:
    if not values:return 0.0
    lo,hi=min(values),max(values)
    if hi<=lo:return 100.0
    raw=(value-lo)/(hi-lo)*100.0
    return round(raw if higher_better else 100.0-raw,1)

def allocate_portfolio_capital(portfolio:dict[str,Any], available_capital:float, weights:dict[str,float]|None=None)->dict[str,Any]:
    weights=weights or DEFAULT_WEIGHTS; rows=[dict(x) for x in portfolio.get('ranking',[]) or []]; capital=max(0.0,_n(available_capital))
    if not rows:return {'portfolio_capital_allocation_version':ENGINE_VERSION,'status':'GEEN INVESTERINGSDATA','available_capital':capital,'allocations':[],'unallocated_capital':capital}
    risk_vals=[_n(r.get('risk_score')) for r in rows]; reserve_vals=[_n(r.get('reserve_per_apartment')) for r in rows]; lcc_vals=[_n(r.get('lcc_per_apartment')) for r in rows]; sustain_vals=[_n(r.get('sustainability_score')) for r in rows]; loop_vals=[_n(r.get('closed_loop_score')) for r in rows]
    candidates=[]
    for r in rows:
        risk=_norm(_n(r.get('risk_score')),risk_vals,True); affordability=_norm(_n(r.get('reserve_per_apartment')),reserve_vals,False); lcc=_norm(_n(r.get('lcc_per_apartment')),lcc_vals,False); sustainability=_norm(_n(r.get('sustainability_score')),sustain_vals,True); urgency=round((risk+_norm(_n(r.get('closed_loop_score')),loop_vals,False))/2,1)
        score=round(urgency*weights['urgency']+risk*weights['risk']+affordability*weights['affordability']+lcc*weights['lcc']+sustainability*weights['sustainability'],1)
        need=max(0.0,_n(r.get('lcc_30_year'))-_n(r.get('reserve')))
        if need<=0: need=max(0.0,_n(r.get('lcc_per_apartment'))*max(1,int(_n(r.get('apartments')))))
        candidates.append({'name':r.get('name',''),'priority_score':score,'investment_need':round(need,2),'scores':{'urgency':urgency,'risk':risk,'affordability':affordability,'lcc':lcc,'sustainability':sustainability},'portfolio_rank':r.get('rank',0)})
    candidates=sorted(candidates,key=lambda x:(-x['priority_score'],-x['investment_need'],x['name']))
    remaining=capital; allocations=[]
    for i,c in enumerate(candidates,1):
        allocated=min(remaining,c['investment_need']); remaining=round(remaining-allocated,2)
        allocations.append({**c,'capital_rank':i,'allocated_capital':round(allocated,2),'funding_gap':round(max(0,c['investment_need']-allocated),2),'funding_status':'VOLLEDIG' if allocated>=c['investment_need'] and c['investment_need']>0 else ('GEDEELTELIJK' if allocated>0 else 'NIET GEFINANCIERD')})
    funded=sum(1 for a in allocations if a['funding_status']=='VOLLEDIG'); partial=sum(1 for a in allocations if a['funding_status']=='GEDEELTELIJK')
    return {'portfolio_capital_allocation_version':ENGINE_VERSION,'status':'ALLOCATIEVOORSTEL BESCHIKBAAR','available_capital':round(capital,2),'allocated_capital':round(capital-remaining,2),'unallocated_capital':round(remaining,2),'fully_funded_count':funded,'partially_funded_count':partial,'weights':weights,'allocations':allocations,'human_decision_required':True,'automatic_commitment':False,'next_action':'Leg het allocatievoorstel met financieringsgaten ter besluitvorming voor aan portefeuillebestuur/ALV.'}
