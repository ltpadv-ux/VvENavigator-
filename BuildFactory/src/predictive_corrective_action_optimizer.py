"""Enterprise 9.6 Predictive Corrective Action Optimizer.

Generates and ranks corrective paths when strategic mandate variance control is
ORANJE or ROOD. Advisory only; no automatic correction or financing commitment.
"""
from __future__ import annotations
from itertools import product
from typing import Any

ENGINE_VERSION='9.6.0'
DEFAULT_ACTION_GRID={
 'extra_contribution_delta':[0.00,0.02,0.04,0.06],
 'extra_mjop_acceleration':[0.00,0.05,0.10],
 'budget_reduction_pct':[0.00,0.05,0.10],
 'sustainability_adjustment':[0.00,0.05,0.10],
}

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def optimize_corrective_actions(variance_control:dict[str,Any], board_mandate:dict[str,Any], actuals:dict[str,Any]|None=None, top_n:int=5)->dict[str,Any]:
    actuals=actuals or {}
    status=variance_control.get('status','')
    if status not in {'ORANJE','ROOD'}:
        return {'predictive_corrective_action_optimizer_version':ENGINE_VERSION,'status':'GEEN CORRECTIE NODIG','ranking':[],'recommended_action':{},'automatic_correction':False,'next_action':'Blijf het actieve mandaat volgen.'}
    mandate=board_mandate.get('mandate',{}) or {}
    variances=variance_control.get('variances',{}) or {}
    current_score=_num(actuals.get('governance_score'))
    score_gap=max(0.0,-_num(variances.get('governance_score_variance')))
    contribution_gap=max(0.0,-_num(variances.get('contribution_delta_variance')))
    mjop_gap=max(0.0,-_num(variances.get('mjop_acceleration_variance')))
    budget_over=max(0.0,_num(variances.get('budget_variance')))
    candidates=[]
    for extra_contrib,extra_mjop,budget_reduction,sustain in product(*DEFAULT_ACTION_GRID.values()):
        recovered_score = current_score + extra_contrib*35 + extra_mjop*25 + sustain*15 + budget_reduction*5
        residual_score_gap=max(0.0,score_gap-(extra_contrib*35 + extra_mjop*25 + sustain*15))
        residual_contribution=max(0.0,contribution_gap-extra_contrib)
        residual_mjop=max(0.0,mjop_gap-extra_mjop)
        residual_budget=max(0.0,budget_over-(budget_reduction*_num(mandate.get('investment_budget_36m'))))
        estimated_cost=round(extra_contrib*36*34*250 + extra_mjop*150000 + sustain*100000,2)
        recovery_penalty=residual_score_gap*3 + residual_contribution*100 + residual_mjop*80 + (1 if residual_budget>0 else 0)*20
        effectiveness=max(0.0,100-recovery_penalty)
        objective=round(effectiveness*0.75 + (100/(1+estimated_cost/100000))*0.25,2)
        candidates.append({'action':{'extra_contribution_delta':extra_contrib,'extra_mjop_acceleration':extra_mjop,'budget_reduction_pct':budget_reduction,'sustainability_adjustment':sustain},'projected_governance_score':round(recovered_score,1),'residuals':{'score_gap':round(residual_score_gap,2),'contribution_gap':round(residual_contribution,4),'mjop_gap':round(residual_mjop,4),'budget_overrun':round(residual_budget,2)},'estimated_corrective_cost':estimated_cost,'effectiveness_score':round(effectiveness,1),'objective_score':objective})
    candidates.sort(key=lambda x:(-x['objective_score'],x['estimated_corrective_cost']))
    ranking=[{'rank':i+1,**row} for i,row in enumerate(candidates[:max(1,top_n)])]
    return {'predictive_corrective_action_optimizer_version':ENGINE_VERSION,'status':'CORRECTIEVOORSTEL BESCHIKBAAR','trigger_status':status,'candidate_count':len(candidates),'ranking':ranking,'recommended_action':ranking[0] if ranking else {},'human_decision_required':True,'automatic_correction':False,'automatic_financing_commitment':False,'next_action':'Laat Bestuur/ALV de aanbevolen herstelroute beoordelen en formeel vastleggen vóór uitvoering.'}
