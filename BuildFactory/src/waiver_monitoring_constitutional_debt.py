"""Enterprise 12.3 Waiver Monitoring & Constitutional Debt Register."""
from __future__ import annotations
from datetime import date, datetime
from typing import Any
ENGINE_VERSION='12.3.0'

def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def _date(v:Any):
 if not v:return None
 try:return datetime.fromisoformat(str(v)).date()
 except Exception:return None

def monitor_waivers(waivers:list[dict[str,Any]]|dict[str,Any], today:date|None=None, repeat_threshold:int=2, age_warning_days:int=90)->dict[str,Any]:
 today=today or date.today(); records=waivers.get('waivers',[]) if isinstance(waivers,dict) else (waivers or [])
 monitored=[]; topics={}; total_impact=0.0; active=expired=review_due=0
 for item in records:
  w=item.get('waiver',item) or {}; status=str(item.get('status',w.get('status',''))).upper(); topic=str(w.get('scope',w.get('proposal_id','algemeen')) or 'algemeen')
  valid_from=_date(w.get('valid_from')); valid_until=_date(w.get('valid_until')); review=_date(w.get('review_date'))
  age=(today-valid_from).days if valid_from else 0; is_expired=bool(valid_until and today>valid_until) or 'VERLOPEN' in status; is_review=bool(review and today>=review) or 'REVIEW' in status; is_active=('ACTIEF' in status) and not is_expired
  impact=_num(w.get('financial_impact_eur')); total_impact+=impact
  active+=1 if is_active else 0; expired+=1 if is_expired else 0; review_due+=1 if is_review else 0
  topics.setdefault(topic,[]).append(w)
  monitored.append({'waiver_id':w.get('waiver_id',''),'scope':topic,'status':'VERLOPEN' if is_expired else ('REVIEW VEREIST' if is_review else ('ACTIEF' if is_active else 'ONVOLLEDIG')),'age_days':age,'financial_impact_eur':impact,'risk_acceptance':w.get('risk_acceptance',''),'review_date':w.get('review_date',''),'valid_until':w.get('valid_until','')})
 repeated=[{'scope':k,'count':len(v),'financial_impact_eur':round(sum(_num(x.get('financial_impact_eur')) for x in v),2)} for k,v in topics.items() if len(v)>=repeat_threshold]
 stale=[x for x in monitored if x['age_days']>=age_warning_days and x['status'] in {'ACTIEF','REVIEW VEREIST'}]
 debt_score=min(100.0, round(active*10 + expired*25 + review_due*15 + len(repeated)*20 + len(stale)*10,1))
 if debt_score>=70: debt_level='ROOD'
 elif debt_score>=40: debt_level='ORANJE'
 elif debt_score>0: debt_level='GEEL'
 else: debt_level='GROEN'
 return {'waiver_monitoring_constitutional_debt_version':ENGINE_VERSION,'status':'CONSTITUTIONELE SCHULD KRITIEK' if debt_level=='ROOD' else ('CONSTITUTIONELE SCHULD OPGEBOUWD' if debt_level in {'ORANJE','GEEL'} else 'GEEN CONSTITUTIONELE SCHULD'),'constitutional_debt_score':debt_score,'constitutional_debt_level':debt_level,'active_waivers':active,'expired_waivers':expired,'review_due_waivers':review_due,'total_financial_impact_eur':round(total_impact,2),'repeated_exception_patterns':repeated,'stale_waivers':stale,'waiver_register':monitored,'human_policy_review_required':debt_level in {'ORANJE','ROOD'},'automatic_policy_change':False,'automatic_waiver_extension':False,'automatic_decision':False,'next_action':'Herbeoordeel terugkerende uitzonderingen en bepaal of Constitution/doctrine moet worden aangepast.' if debt_level in {'ORANJE','ROOD'} else 'Blijf actieve waivers volgen tot review of afloop.'}
