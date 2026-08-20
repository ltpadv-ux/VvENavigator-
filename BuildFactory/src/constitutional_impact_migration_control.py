"""Enterprise 12.7 Constitutional Impact Analysis & Migration Control."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='12.7.0'

def _id(*parts:Any)->str:return 'GOVMIG-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def analyze_constitutional_impact(version_result:dict[str,Any], estate:dict[str,Any]|None=None)->dict[str,Any]:
 estate=estate or {}; current=version_result.get('current_version',{}) or {}; previous=str(version_result.get('previous_version','')); new=str(version_result.get('new_version',current.get('version',''))); target=str(version_result.get('applied_target',''))
 if version_result.get('status')!='AMENDMENT GECONTROLEERD VERWERKT':
  return {'constitutional_impact_migration_control_version':ENGINE_VERSION,'status':'GEEN NIEUWE VERSIE VOOR IMPACTANALYSE','migration_plan':[],'activation_ready':False,'automatic_activation':False}
 items=[]
 domains=[('decisions','BESLUITEN'),('mandates','MANDATEN'),('waivers','WAIVERS'),('mjop_rules','MJOP_REGELS'),('financial_limits','FINANCIELE_GRENZEN'),('dashboards','DASHBOARDS')]
 for key,label in domains:
  for obj in estate.get(key,[]) or []:
   ref=str(obj.get('constitution_version',obj.get('framework_version','')))
   affected=bool(ref and ref!=new) or bool(obj.get('depends_on_constitution',False))
   if not affected: continue
   severity='HOOG' if key in {'mandates','financial_limits','waivers'} else ('NORMAAL' if key in {'decisions','mjop_rules'} else 'LAAG')
   action='Herbeoordeel tegen nieuwe constitutionele versie.'
   if key=='mandates': action='Valideer mandaatbevoegdheid en budgetgrenzen opnieuw.'
   elif key=='waivers': action='Toets of waiver nog nodig, geldig en verenigbaar is.'
   elif key=='financial_limits': action='Migreer financiële grens en controleer bestaande verplichtingen.'
   elif key=='mjop_rules': action='Herbereken MJOP-regels en leg afwijkingen opnieuw vast.'
   elif key=='dashboards': action='Werk KPI-definities, thresholds en versiebron bij.'
   items.append({'domain':label,'item_id':obj.get('id',obj.get('mandate_id',obj.get('waiver_id',''))),'name':obj.get('name',obj.get('title','')),'severity':severity,'current_reference':ref,'target_version':new,'recommended_migration':action,'owner':obj.get('owner','Bestuur'),'financial_exposure_eur':_num(obj.get('financial_exposure_eur',obj.get('financial_impact_eur',0))),'migration_complete':bool(obj.get('migration_complete',False))})
 rank={'HOOG':0,'NORMAAL':1,'LAAG':2}; items.sort(key=lambda x:(rank.get(x['severity'],9),-x['financial_exposure_eur']))
 incomplete=[x for x in items if not x['migration_complete']]; high=[x for x in incomplete if x['severity']=='HOOG']; exposure=round(sum(x['financial_exposure_eur'] for x in incomplete),2)
 status='ACTIVATIE GEBLOKKEERD - MIGRATIES VEREIST' if high else ('REVIEW VEREIST VOOR ACTIVATIE' if incomplete else 'ACTIVATIE GEREED')
 return {'constitutional_impact_migration_control_version':ENGINE_VERSION,'migration_id':_id(previous,new,target),'status':status,'previous_version':previous,'new_version':new,'applied_target':target,'affected_item_count':len(items),'open_migration_count':len(incomplete),'high_priority_open_count':len(high),'financial_exposure_eur':exposure,'migration_plan':items,'activation_ready':not incomplete,'human_activation_approval_required':True,'human_legal_governance_review_required':bool(incomplete),'automatic_activation':False,'automatic_migration':False,'automatic_decision':False,'next_action':'Voltooi alle migraties en laat de nieuwe versie formeel activeren.' if incomplete else 'Laat Bestuur/ALV de nieuwe versie formeel activeren.'}
