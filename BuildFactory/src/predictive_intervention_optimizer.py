"""Enterprise 9.2 Predictive Intervention Optimizer.

Searches combinations of contribution change, MJOP acceleration, financing and
sustainability investment and ranks them on future VvE Health & Governance
score versus estimated 36-month cost. Advisory only; no automatic execution.
"""
from __future__ import annotations
from itertools import product
from typing import Any

from executive_digital_twin import build_executive_digital_twin

ENGINE_VERSION='9.2.0'
DEFAULT_GRID={
 'contribution_delta':[0.00,0.03,0.05,0.08,0.10],
 'mjop_acceleration':[0.00,0.05,0.10,0.15,0.20],
 'financing_share':[0.00,0.25,0.50,0.75],
 'sustainability_investment':[0.00,0.10,0.20,0.30],
}

def _cost(a:dict[str,float], apartments:int, base_monthly:float)->float:
    contribution=max(0.0,a['contribution_delta'])*base_monthly*apartments*36
    mjop=max(0.0,a['mjop_acceleration'])*250000
    sustainability=max(0.0,a['sustainability_investment'])*300000
    financing_cost=max(0.0,a['financing_share'])*(mjop+sustainability)*0.06*3
    return round(contribution+mjop+sustainability+financing_cost,2)

def optimize_predictive_interventions(governance_os:dict[str,Any], apartments:int=34, base_monthly_contribution:float=250.0, grid:dict[str,list[float]]|None=None, top_n:int=10)->dict[str,Any]:
    g=grid or DEFAULT_GRID; candidates=[]
    keys=('contribution_delta','mjop_acceleration','financing_share','sustainability_investment')
    for values in product(*(g[k] for k in keys)):
        a=dict(zip(keys,values))
        scenario={
          'inflation_delta':0.01,
          'interest_delta':round(0.01 + a['financing_share']*0.015,4),
          'contribution_delta':a['contribution_delta'],
          'mjop_acceleration':a['mjop_acceleration'],
          'sustainability_investment':a['sustainability_investment'],
        }
        twin=build_executive_digital_twin(governance_os,{'OPT':scenario})
        row=next(x for x in twin['projections'] if x['scenario']=='OPT')
        score36=float(row['score_36m']); cost=_cost(a,apartments,base_monthly_contribution)
        efficiency=round(score36/(1+cost/100000),2)
        objective=round(score36*0.75 + efficiency*0.25,2)
        candidates.append({'intervention':a,'score_12m':row['horizons'][0]['score'],'score_24m':row['horizons'][1]['score'],'score_36m':score36,'status_36m':row['status_36m'],'estimated_36m_cost':cost,'cost_efficiency':efficiency,'objective_score':objective})
    candidates.sort(key=lambda x:(-x['objective_score'],-x['score_36m'],x['estimated_36m_cost']))
    ranked=[]
    for i,x in enumerate(candidates[:max(1,top_n)],1): ranked.append({'rank':i,**x})
    best=ranked[0]
    return {'predictive_intervention_optimizer_version':ENGINE_VERSION,'candidate_count':len(candidates),'top_count':len(ranked),'ranking':ranked,'recommended_intervention':best,'human_decision_required':True,'automatic_execution':False,'automatic_financing_commitment':False,'objective':'Maximaliseer toekomstige governance/health score tegen zo laag mogelijke 36-maands kosten.','next_action':'Laat Bestuur/ALV de aanbevolen combinatie toetsen op betaalbaarheid, juridische bevoegdheid en uitvoerbaarheid vóór besluitvorming.'}
