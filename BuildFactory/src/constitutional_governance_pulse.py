"""Enterprise 13.1 Constitutional Governance Pulse & Executive Exception Feed."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='13.1.0'
DECISION_RANK={'BEHOUDEN':0,'HERSTELLEN':1,'ROLLBACK':2}

def _id(*parts:Any)->str:return 'GOVPLS-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def build_governance_pulse(current:dict[str,Any], previous:dict[str,Any]|None=None, current_amendments:list[dict[str,Any]]|None=None, previous_amendments:list[dict[str,Any]]|None=None, debt_materiality:float=10.0, health_materiality:float=5.0)->dict[str,Any]:
 previous=previous or {}; current_amendments=current_amendments or []; previous_amendments=previous_amendments or []
 exceptions=[]; changes=[]
 cur_gate=str(current.get('decision_gate','GO')).upper(); prev_gate=str(previous.get('decision_gate','GO')).upper()
 if cur_gate=='BLOCK' and prev_gate!='BLOCK': exceptions.append({'priority':'KRITIEK','type':'NEW_BLOCK','message':'Nieuwe constitutionele BLOCK sinds vorige bestuursrun.'})
 cur_w=int(_num(current.get('active_waivers',0))); prev_w=int(_num(previous.get('active_waivers',0))); wd=cur_w-prev_w
 if wd>0: exceptions.append({'priority':'HOOG','type':'NEW_WAIVERS','delta':wd,'message':f'{wd} nieuwe actieve waiver(s) sinds vorige run.'})
 cur_debt=_num(current.get('constitutional_debt_score',0)); prev_debt=_num(previous.get('constitutional_debt_score',0)); debt_delta=round(cur_debt-prev_debt,1)
 if debt_delta>=debt_materiality: exceptions.append({'priority':'HOOG','type':'DEBT_INCREASE','delta':debt_delta,'message':f'Constitutional Debt Score steeg met {debt_delta} punten.'})
 cur_mig=int(_num(current.get('open_migrations',0))); prev_mig=int(_num(previous.get('open_migrations',0))); mig_delta=cur_mig-prev_mig
 if mig_delta>0: exceptions.append({'priority':'HOOG','type':'MIGRATION_DELAY','delta':mig_delta,'message':f'{mig_delta} extra open migratie(s) sinds vorige run.'})
 cur_dec=str(current.get('assurance_decision','BEHOUDEN')).upper(); prev_dec=str(previous.get('assurance_decision','BEHOUDEN')).upper()
 if DECISION_RANK.get(cur_dec,0)>DECISION_RANK.get(prev_dec,0): exceptions.append({'priority':'KRITIEK' if cur_dec=='ROLLBACK' else 'HOOG','type':'ASSURANCE_ESCALATION','from':prev_dec,'to':cur_dec,'message':f'Assurance-beslissing verslechterde van {prev_dec} naar {cur_dec}.'})
 cur_h=_num(current.get('constitutional_health_score',0)); prev_h=_num(previous.get('constitutional_health_score',cur_h)); health_delta=round(cur_h-prev_h,1)
 if health_delta<=-abs(health_materiality): exceptions.append({'priority':'HOOG','type':'HEALTH_DROP','delta':health_delta,'message':f'Constitutional Health Score daalde met {abs(health_delta)} punten.'})
 prev_ids={str(x.get('amendment_id',x.get('id',''))) for x in previous_amendments}; new_amendments=[x for x in current_amendments if str(x.get('amendment_id',x.get('id',''))) not in prev_ids]
 if new_amendments: exceptions.append({'priority':'NORMAAL','type':'NEW_AMENDMENTS','count':len(new_amendments),'message':f'{len(new_amendments)} nieuw(e) constitutional amendment(s) sinds vorige run.'})
 tracked=[('decision_gate',prev_gate,cur_gate),('active_waivers',prev_w,cur_w),('constitutional_debt_score',prev_debt,cur_debt),('open_migrations',prev_mig,cur_mig),('assurance_decision',prev_dec,cur_dec),('constitutional_health_score',prev_h,cur_h)]
 for field,before,after in tracked:
  if before!=after: changes.append({'field':field,'previous':before,'current':after})
 critical=any(x['priority']=='KRITIEK' for x in exceptions); status='KRITIEKE WIJZIGING' if critical else ('WIJZIGINGEN' if exceptions else 'STABIEL')
 return {'constitutional_governance_pulse_version':ENGINE_VERSION,'pulse_id':_id(current.get('tower_id',''),previous.get('tower_id',''),len(exceptions)),'status':status,'exception_count':len(exceptions),'critical_exception_count':sum(1 for x in exceptions if x['priority']=='KRITIEK'),'executive_exception_feed':exceptions,'material_changes':changes,'new_amendments':new_amendments,'debt_delta':debt_delta,'waiver_delta':wd,'migration_delta':mig_delta,'health_delta':health_delta,'human_board_review_required':bool(exceptions),'automatic_decision':False,'automatic_execution':False,'automatic_rollback':False,'next_action':'Behandel kritieke uitzonderingen eerst.' if critical else ('Beoordeel de nieuwe governance-wijzigingen.' if exceptions else 'Geen materiële wijziging sinds vorige bestuursrun.')}
