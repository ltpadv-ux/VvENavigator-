"""Enterprise 13.4 Preventive Governance Intervention Planner."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='13.4.0'

def _id(*parts:Any)->str:return 'GOVPIP-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def build_preventive_governance_plan(forecast:dict[str,Any], current:dict[str,Any], owners:dict[str,str]|None=None)->dict[str,Any]:
 owners=owners or {}; targets=forecast.get('threshold_forecast_runs',{}) or {}; actions=[]
 def add(metric:str,action:str,owner:str,effect:dict[str,float],priority:str='HOOG'):
  runs=targets.get(metric)
  if runs is not None and runs<=3:
   actions.append({'metric':metric,'priority':'KRITIEK' if runs<=1 else priority,'runs_to_threshold':runs,'owner':owners.get(metric,owner),'recommended_action':action,'expected_effect':effect})
 add('debt_red','Versnel afbouw van waivers en sluit achterstallige constitutionele reviews.','Bestuur',{'debt_score_delta':-15,'health_score_delta':5,'waiver_delta':-1})
 add('debt_orange','Start vroegtijdige debt-remediation en normaliseer terugkerende uitzonderingen.','Bestuur',{'debt_score_delta':-10,'health_score_delta':4})
 add('health_red','Voer gerichte governance-herstelacties uit op compliance, migraties en assurance.','Bestuur',{'health_score_delta':12,'debt_score_delta':-5})
 add('health_orange','Start preventieve governance-review en herstel zwakke controls.','Bestuur',{'health_score_delta':8})
 add('waiver_pressure','Beoordeel actieve waivers, beëindig onnodige uitzonderingen en voorkom verlenging zonder nieuw besluit.','Bestuur',{'waiver_delta':-1,'debt_score_delta':-8})
 add('migration_pressure','Prioriteer constitutionele migraties en wijs per migratie een eigenaar en harde deadline toe.','Projecteigenaar',{'open_migrations_delta':-2,'health_score_delta':3})
 add('assurance_escalation','Start post-activation herstelreview vóór escalatie naar rollback.','Bestuur',{'assurance_risk_delta':-1,'health_score_delta':5})
 current_debt=_num(current.get('constitutional_debt_score',0)); current_health=_num(current.get('constitutional_health_score',100)); current_waivers=_num(current.get('active_waivers',0)); current_migrations=_num(current.get('open_migrations',0))
 debt_delta=sum(_num(a['expected_effect'].get('debt_score_delta',0)) for a in actions); health_delta=sum(_num(a['expected_effect'].get('health_score_delta',0)) for a in actions); waiver_delta=sum(_num(a['expected_effect'].get('waiver_delta',0)) for a in actions); migration_delta=sum(_num(a['expected_effect'].get('open_migrations_delta',0)) for a in actions)
 projected={'constitutional_debt_score':max(0,round(current_debt+debt_delta,1)),'constitutional_health_score':min(100,round(current_health+health_delta,1)),'active_waivers':max(0,int(current_waivers+waiver_delta)),'open_migrations':max(0,int(current_migrations+migration_delta))}
 nearest=forecast.get('forecast_horizon_runs'); shift=0
 if actions and nearest is not None:
  protective=max(0,-debt_delta)/10 + max(0,health_delta)/8 + max(0,-waiver_delta) + max(0,-migration_delta)
  shift=max(1,int(round(protective)))
 status='PREVENTIEF INTERVENTIEPLAN VEREIST' if actions else 'GEEN PREVENTIEVE INTERVENTIE NODIG'
 return {'preventive_governance_intervention_planner_version':ENGINE_VERSION,'plan_id':_id(current.get('tower_id',''),forecast.get('status',''),len(actions)),'status':status,'action_count':len(actions),'actions':actions,'current_state':{'constitutional_debt_score':current_debt,'constitutional_health_score':current_health,'active_waivers':int(current_waivers),'open_migrations':int(current_migrations)},'projected_state_after_plan':projected,'estimated_threshold_shift_runs':shift,'estimated_new_horizon_runs':None if nearest is None else nearest+shift,'human_board_approval_required':bool(actions),'human_legal_governance_review_required':any(a['priority']=='KRITIEK' for a in actions),'automatic_intervention':False,'automatic_policy_change':False,'automatic_decision':False,'automatic_execution':False,'next_action':'Laat Bestuur/ALV het preventieve interventieplan prioriteren, begroten en mandateren.' if actions else 'Blijf forecast en trend periodiek volgen.'}
