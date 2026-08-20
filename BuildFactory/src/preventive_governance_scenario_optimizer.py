"""Enterprise 13.5 Preventive Governance Scenario Optimizer."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='13.5.0'

def _id(*parts:Any)->str:return 'GOVOPT-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def optimize_preventive_governance_scenarios(plan:dict[str,Any], scenarios:list[dict[str,Any]]|None=None, budget_limit_eur:float|None=None)->dict[str,Any]:
 actions=plan.get('actions',[]) or []
 if scenarios is None:
  scenarios=[
   {'name':'MINIMAAL','action_indices':list(range(min(1,len(actions)))),'cost_eur':2500,'feasibility_score':95},
   {'name':'GEBALANCEERD','action_indices':list(range(min(3,len(actions)))),'cost_eur':7500,'feasibility_score':85},
   {'name':'VERSNELD','action_indices':list(range(len(actions))),'cost_eur':15000,'feasibility_score':70},
  ]
 rows=[]
 for s in scenarios:
  selected=[actions[i] for i in s.get('action_indices',[]) if isinstance(i,int) and 0<=i<len(actions)]
  debt=sum(max(0,-_num(a.get('expected_effect',{}).get('debt_score_delta',0))) for a in selected)
  health=sum(max(0,_num(a.get('expected_effect',{}).get('health_score_delta',0))) for a in selected)
  waiver=sum(max(0,-_num(a.get('expected_effect',{}).get('waiver_delta',0))) for a in selected)
  migration=sum(max(0,-_num(a.get('expected_effect',{}).get('open_migrations_delta',0))) for a in selected)
  effect=round(min(100,debt*2+health*2+waiver*12+migration*8),1)
  cost=max(0,_num(s.get('cost_eur',0))); feasibility=max(0,min(100,_num(s.get('feasibility_score',75))))
  shift=round(max(0,debt/10+health/8+waiver+migration),1)
  value=round((effect*1000/cost),2) if cost>0 else (999.0 if effect>0 else 0.0)
  within_budget=True if budget_limit_eur is None else cost<=budget_limit_eur
  score=round(effect*0.40+feasibility*0.25+min(100,value)*0.20+min(100,shift*15)*0.15-(0 if within_budget else 25),1)
  rows.append({'scenario_id':_id(plan.get('plan_id',''),s.get('name','')),'name':s.get('name','SCENARIO'),'action_count':len(selected),'cost_eur':cost,'feasibility_score':feasibility,'effect_score':effect,'threshold_shift_runs':shift,'value_per_1000_eur':value,'within_budget':within_budget,'optimization_score':score,'selected_actions':[a.get('recommended_action','') for a in selected]})
 rows.sort(key=lambda x:(not x['within_budget'],-x['optimization_score'],x['cost_eur']))
 best=rows[0] if rows else None
 status='GEEN SCENARIOS BESCHIKBAAR' if not rows else ('VOORKEURSSCENARIO BESCHIKBAAR' if best.get('within_budget',False) else 'GEEN SCENARIO BINNEN BUDGET')
 return {'preventive_governance_scenario_optimizer_version':ENGINE_VERSION,'optimizer_id':_id(plan.get('plan_id',''),len(rows)),'status':status,'scenario_count':len(rows),'budget_limit_eur':budget_limit_eur,'ranked_scenarios':rows,'recommended_scenario':best,'human_board_decision_required':bool(rows),'human_budget_approval_required':bool(best and best.get('cost_eur',0)>0),'automatic_selection':False,'automatic_budget_commitment':False,'automatic_decision':False,'automatic_execution':False,'next_action':'Laat Bestuur/ALV het voorkeurscenario beoordelen op effect, kosten, uitvoerbaarheid en governance-risico.' if rows else 'Definieer minimaal één uitvoerbaar interventiescenario.'}
