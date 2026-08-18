"""Track approved intervention execution and close only after delivery and benefits are evidenced."""
from __future__ import annotations
from datetime import datetime, timezone, date
from typing import Any

ENGINE_VERSION='6.9.0'

def _num(v:Any, default:float=0.0)->float:
    try: return float(v)
    except (TypeError,ValueError): return default

def track_execution_and_benefits(execution:dict[str,Any], report:dict[str,Any], existing:dict[str,Any]|None=None)->dict[str,Any]:
    now=datetime.now(timezone.utc).isoformat(); existing=existing or {}; mandate=execution.get('mandate',{}) or {}
    if execution.get('status')!='MANDAAT ACTIEF' or not mandate:
        return {'execution_benefits_version':ENGINE_VERSION,'generated_at':now,'status':'GEEN ACTIEF MANDAAT','tracking':{},'benefits':{},'closure':{'eligible':False,'status':'NIET VAN TOEPASSING'},'next_action':'Wacht op een goedgekeurd interventiemandaat.'}
    prev=existing.get('tracking',{}) or {}; tower=((report.get('governance_control_tower',{}) or {}).get('kpis',{}) or {})
    progress=max(0,min(100,_num(prev.get('progress_percent',0)))); spent=max(0,_num(prev.get('spent_amount',0))); budget=max(0,_num(mandate.get('budget_ceiling',0)))
    deadline=str(prev.get('execution_deadline') or mandate.get('execution_deadline') or ''); overdue=False
    if deadline:
        try: overdue=date.fromisoformat(deadline).isoformat()<date.today().isoformat() and progress<100
        except ValueError: overdue=False
    tracking={'mandate_id':mandate.get('mandate_id',''),'owner':prev.get('owner') or mandate.get('owner',''),'progress_percent':progress,'spent_amount':round(spent,2),'budget_ceiling':round(budget,2),'budget_remaining':round(budget-spent,2),'budget_within_mandate':spent<=budget if budget>0 else True,'execution_deadline':deadline,'deadline_overdue':overdue,'status':'GEREED VOOR EFFECTCONTROLE' if progress>=100 else 'IN UITVOERING','last_update':now}
    actual_reserve=_num(tower.get('reserve',prev.get('actual_reserve',0))); target_reserve=_num(mandate.get('projected_reserve',0)); actual_monthly=_num(tower.get('monthly_per_apartment',prev.get('actual_monthly_contribution',0))); target_monthly=_num(mandate.get('monthly_contribution_per_apartment',0)); actual_risk=_num(prev.get('actual_risk_delta',0)); target_risk=_num(mandate.get('target_risk_delta',0)); actual_mjop=_num(prev.get('actual_mjop_shift_months',0)); target_mjop=_num(mandate.get('mjop_shift_months',0))
    reserve_ok=(actual_reserve>=target_reserve) if target_reserve>0 else True; monthly_ok=(actual_monthly<=target_monthly) if target_monthly>0 else True; risk_ok=(actual_risk<=target_risk) if target_risk<0 else True; mjop_ok=(actual_mjop<=target_mjop) if target_mjop<0 else (actual_mjop>=target_mjop if target_mjop>0 else True)
    benefits={'actual_reserve':round(actual_reserve,2),'target_reserve':round(target_reserve,2),'reserve_realized':reserve_ok,'actual_monthly_contribution':round(actual_monthly,2),'target_monthly_contribution':round(target_monthly,2),'monthly_target_realized':monthly_ok,'actual_risk_delta':actual_risk,'target_risk_delta':target_risk,'risk_reduction_realized':risk_ok,'actual_mjop_shift_months':actual_mjop,'target_mjop_shift_months':target_mjop,'mjop_effect_realized':mjop_ok}
    benefit_checks=[reserve_ok,monthly_ok,risk_ok,mjop_ok]; realized=sum(1 for x in benefit_checks if x); benefits['realization_score']=round(realized/len(benefit_checks)*100,1)
    eligible=progress>=100 and tracking['budget_within_mandate'] and not overdue and all(benefit_checks); previous_closed=(existing.get('closure',{}) or {}).get('status')=='GESLOTEN'
    closure={'eligible':eligible or previous_closed,'status':'GESLOTEN' if eligible or previous_closed else 'OPEN','closed_at':(existing.get('closure',{}) or {}).get('closed_at') or (now if eligible else ''),'evidence':['uitvoering 100%','binnen budget','deadline op orde','reserve-effect','maandbijdrage-effect','risicoreductie','MJOP-effect'] if eligible else []}
    overall='EFFECT BEWEZEN' if closure['status']=='GESLOTEN' else 'EFFECTCONTROLE' if progress>=100 else 'IN UITVOERING'
    return {'execution_benefits_version':ENGINE_VERSION,'generated_at':now,'status':overall,'tracking':tracking,'benefits':benefits,'closure':closure,'next_action':'Interventie aantoonbaar gerealiseerd en gesloten.' if closure['status']=='GESLOTEN' else ('Vul ontbrekend effectbewijs aan en herstel afwijkingen.' if progress>=100 else 'Werk voortgang en besteding bij; blijf budget, deadline en KPI-effecten volgen.')}
