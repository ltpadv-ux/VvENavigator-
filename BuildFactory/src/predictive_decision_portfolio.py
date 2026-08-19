"""Enterprise 9.3 Predictive Decision Portfolio & Pareto Frontier.

Builds a board-ready choice set from predictive intervention candidates using
multi-objective Pareto dominance across cost, contribution pressure, future
score, risk reduction and sustainability impact. Advisory only.
"""
from __future__ import annotations
from typing import Any

ENGINE_VERSION='9.3.0'

def _risk_reduction(intervention:dict[str,Any])->float:
    return round(float(intervention.get('mjop_acceleration',0) or 0)*60 + float(intervention.get('sustainability_investment',0) or 0)*40,1)

def _sustainability(intervention:dict[str,Any])->float:
    return round(float(intervention.get('sustainability_investment',0) or 0)*100,1)

def _contribution_pressure(intervention:dict[str,Any])->float:
    return round(float(intervention.get('contribution_delta',0) or 0)*100,1)

def _dominates(a:dict[str,Any],b:dict[str,Any])->bool:
    # Maximize: score, risk_reduction, sustainability. Minimize: cost, contribution_pressure.
    not_worse=(a['score_36m']>=b['score_36m'] and a['risk_reduction']>=b['risk_reduction'] and a['sustainability_impact']>=b['sustainability_impact'] and a['estimated_36m_cost']<=b['estimated_36m_cost'] and a['contribution_pressure']<=b['contribution_pressure'])
    strictly=(a['score_36m']>b['score_36m'] or a['risk_reduction']>b['risk_reduction'] or a['sustainability_impact']>b['sustainability_impact'] or a['estimated_36m_cost']<b['estimated_36m_cost'] or a['contribution_pressure']<b['contribution_pressure'])
    return not_worse and strictly

def build_predictive_decision_portfolio(optimizer:dict[str,Any])->dict[str,Any]:
    rows=[]
    for src in optimizer.get('ranking',[]) or []:
        iv=src.get('intervention',{}) or {}
        rows.append({**src,'risk_reduction':_risk_reduction(iv),'sustainability_impact':_sustainability(iv),'contribution_pressure':_contribution_pressure(iv)})
    frontier=[]
    for r in rows:
        if not any(_dominates(o,r) for o in rows if o is not r): frontier.append(r)
    frontier.sort(key=lambda x:(-x['score_36m'],x['estimated_36m_cost'],x['contribution_pressure']))
    for i,r in enumerate(frontier,1): r['pareto_rank']=i
    def pick(key,reverse=False):
        return (sorted(frontier,key=lambda x:x[key],reverse=reverse)[0] if frontier else {})
    archetypes={
      'HOOGSTE GOVERNANCE SCORE':pick('score_36m',True),
      'LAAGSTE KOSTEN':pick('estimated_36m_cost'),
      'LAAGSTE BIJDRAGEDRUK':pick('contribution_pressure'),
      'HOOGSTE RISICOREDUCTIE':pick('risk_reduction',True),
      'HOOGSTE VERDUURZAMING':pick('sustainability_impact',True),
    }
    unique=[]; seen=set()
    for label,row in archetypes.items():
        if not row: continue
        key=str(row.get('intervention'))
        if key in seen: continue
        seen.add(key); unique.append({'label':label,**row})
    return {'predictive_decision_portfolio_version':ENGINE_VERSION,'candidate_count':len(rows),'pareto_count':len(frontier),'pareto_frontier':frontier,'board_choice_cards':unique,'objectives':['max governance score','min cost','min contribution pressure','max risk reduction','max sustainability impact'],'human_decision_required':True,'automatic_selection':False,'next_action':'Gebruik de Pareto-frontier als bestuurlijke keuzekaart en laat Bestuur/ALV expliciet kiezen welke trade-off het best past bij de VvE-strategie.'}
