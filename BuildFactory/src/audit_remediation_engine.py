"""Turn failed treasury assurance controls into owned remediation and re-test actions."""
from __future__ import annotations
from datetime import date, timedelta
from hashlib import sha256
from typing import Any

ENGINE_VERSION='8.7.0'
CONTROL_ACTIONS={
 'FUNCTIESCHEIDING':('Scheid goedkeuring en uitvoering en leg rollen aantoonbaar vast.','Governance'),
 'BESLUITKWALITEIT':('Vul besluit, bevoegdheid en onderbouwing volledig aan.','Bestuur'),
 'BUDGETCONTROLE':('Herstel budgetgrens, verklaar overschrijding en borg autorisatie.','Penningmeester'),
 'UITVOERINGSBEWIJS':('Voeg verifieerbaar uitvoeringsbewijs toe aan de actie.','Actie-eigenaar'),
 'EFFECTMETING':('Voer effectmeting uit en documenteer de controleresultaten.','Control'),
 'SLUITINGSCONTROLE':('Heropen sluiting en laat menselijke effectbeoordeling vastleggen.','Bestuur/ALV'),
 'LINEAGE COMPLEET':('Herstel ontbrekende koppelingen in de audit lineage.','Control'),
}

def _id(lineage:str,control:str)->str:
 return 'TRREM-'+sha256(f'{lineage}|{control}'.encode()).hexdigest()[:10].upper()

def build_audit_remediation(report:dict[str,Any], existing:dict[str,Any]|None=None, deadline_days:int=30)->dict[str,Any]:
 assurance=report.get('treasury_audit_assurance',{}) or {}; existing=existing or {}; old={x.get('remediation_id'):x for x in existing.get('actions',[]) or []}; actions=[]
 for result in assurance.get('results',[]) or []:
  lineage=result.get('lineage_id',''); score=float(result.get('assurance_score',0) or 0)
  for control in result.get('failed_controls',[]) or []:
   rid=_id(lineage,control); prior=old.get(rid,{})
   action,default_owner=CONTROL_ACTIONS.get(control,('Herstel de control en documenteer de maatregel.','Control'))
   priority='KRITIEK' if score<50 else ('HOOG' if score<70 else 'NORMAAL')
   status=prior.get('status','OPEN'); retest=prior.get('retest',{}) or {}
   if retest.get('passed') is True: status='HERSTEL BEWEZEN'
   actions.append({'remediation_id':rid,'lineage_id':lineage,'agenda_id':result.get('agenda_id',''),'control':control,'priority':priority,'action':action,'owner':prior.get('owner',default_owner),'deadline':prior.get('deadline',(date.today()+timedelta(days=deadline_days)).isoformat()),'status':status,'evidence':prior.get('evidence',[]),'retest':retest})
 open_count=sum(x['status']!='HERSTEL BEWEZEN' for x in actions); proven=len(actions)-open_count
 status='GEEN HERSTELACTIES' if not actions else ('CONTROLS HERSTELD' if open_count==0 else 'HERSTELACTIES OPEN')
 return {'audit_remediation_version':ENGINE_VERSION,'status':status,'action_count':len(actions),'open_count':open_count,'proven_count':proven,'actions':actions,'target_assurance_score':90,'human_retest_required':True,'automatic_closure':False,'next_action':'Laat herstelde controls menselijk her-testen en sluit alleen met bewijs.' if actions else 'Geen failed controls; geen remediation nodig.'}
