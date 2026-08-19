"""Create a 12/24/36-month governance improvement roadmap from maturity gaps."""
from __future__ import annotations
from datetime import date
from hashlib import sha256
from typing import Any

ENGINE_VERSION='8.9.0'
DEFAULT_TARGET=90
DOMAIN_ACTIONS={
 'governance':('Bestuurlijke stuurkring en besluitdiscipline versterken','Bestuur'),
 'finance':('Financiële gezondheid, reservebeleid en prognosekwaliteit verbeteren','Penningmeester'),
 'mjop':('MJOP-datakwaliteit, risico- en lifecycle-sturing aanscherpen','Technisch beheer'),
 'treasury':('Liquiditeit, DSCR, convenanten en treasury forecasting versterken','Penningmeester'),
 'audit':('Control testing, evidence en audit assurance structureel verbeteren','Control / accountant'),
 'decision_execution':('Besluituitvoering, eigenaarschap en bewijsdiscipline verhogen','Bestuur / beheerder'),
}

def _id(domain:str,horizon:int)->str:
 return 'GOVRM-'+sha256(f'{domain}|{horizon}'.encode()).hexdigest()[:10].upper()

def build_governance_improvement_roadmap(maturity:dict[str,Any], existing:dict[str,Any]|None=None, target:int=DEFAULT_TARGET)->dict[str,Any]:
 existing=existing or {}; prior={x.get('roadmap_id'):x for x in existing.get('actions',[]) or []}; scores=maturity.get('domain_scores',{}) or {}; actions=[]
 for domain,score_raw in scores.items():
  score=float(score_raw or 0)
  if score>=target: continue
  gap=max(0, target-score)
  horizon=12 if gap<=10 else (24 if gap<=25 else 36)
  rid=_id(domain,horizon); old=prior.get(rid,{})
  action,owner=DOMAIN_ACTIONS.get(domain,('Verbeter dit governance-domein','Bestuur'))
  investment=round(gap*500,2)
  milestone_target=round(min(target,score+gap*(0.5 if horizon==36 else 0.67 if horizon==24 else 1.0)),1)
  actions.append({'roadmap_id':rid,'domain':domain,'current_score':round(score,1),'target_score':target,'gap':round(gap,1),'horizon_months':horizon,'action':old.get('action',action),'owner':old.get('owner',owner),'estimated_investment':old.get('estimated_investment',investment),'status':old.get('status','GEPLAND'),'progress_percent':float(old.get('progress_percent',0) or 0),'milestones':[{'month':min(12,horizon),'target_score':milestone_target},{'month':horizon,'target_score':target}],'measure_every_months':6,'evidence':old.get('evidence',[])})
 actions.sort(key=lambda x:(-x['gap'],x['domain']))
 total=round(sum(float(x['estimated_investment'] or 0) for x in actions),2); open_count=sum(x['status']!='AFGEROND' for x in actions)
 status='DOELNIVEAU BEREIKT' if not actions else ('VERBETERPROGRAMMA ACTIEF' if any(x['progress_percent']>0 for x in actions) else 'VERBETERPROGRAMMA GEREED')
 return {'governance_improvement_roadmap_version':ENGINE_VERSION,'generated_on':date.today().isoformat(),'status':status,'current_maturity_index':maturity.get('maturity_index',0),'target_maturity_index':target,'action_count':len(actions),'open_count':open_count,'total_estimated_investment':total,'actions':actions,'measurement_cadence_months':6,'human_approval_required':bool(actions),'automatic_execution':False,'next_action':'Borg maturity ≥90 en blijf halfjaarlijks meten.' if not actions else 'Laat Bestuur/ALV de roadmap prioriteren, budgetteren en eigenaarschap vastleggen.'}
