"""Enterprise 12.9 Post-Activation Assurance & Rollback Decision Control."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='12.9.0'

def _id(*parts:Any)->str:return 'GOVPAR-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def assess_post_activation(cutover_result:dict[str,Any], evidence:dict[str,Any]|None=None)->dict[str,Any]:
 evidence=evidence or {}; cutover=cutover_result.get('cutover',{}) or {}
 if cutover_result.get('status')!='CUTOVER GEREED VOOR FORMELE ACTIVATIE' and not evidence.get('activated',False):
  return {'post_activation_assurance_rollback_control_version':ENGINE_VERSION,'status':'GEEN ACTIEVE CUTOVER VOOR REVIEW','decision':'GEEN','automatic_rollback':False,'automatic_decision':False}
 compliance=_num(evidence.get('compliance_score',100)); kpi=_num(evidence.get('kpi_stability_score',100)); incidents=int(_num(evidence.get('critical_incidents',0))); waivers=int(_num(evidence.get('new_waivers',0))); migration_issues=int(_num(evidence.get('migration_issues',0))); control_failures=int(_num(evidence.get('control_failures',0)))
 score=max(0.0,round(compliance*0.35+kpi*0.25+max(0,100-incidents*30)*0.15+max(0,100-waivers*15)*0.10+max(0,100-migration_issues*20)*0.10+max(0,100-control_failures*25)*0.05,1))
 blockers=[]; repairs=[]
 if compliance<70: blockers.append('Compliance-score onder 70.')
 if incidents>=2: blockers.append('Meerdere kritieke incidenten na activatie.')
 if control_failures>=2: blockers.append('Meerdere control failures na activatie.')
 if kpi<80: repairs.append('KPI-stabiliteit onder doelwaarde.')
 if waivers>0: repairs.append('Nieuwe waivers ontstaan na activatie.')
 if migration_issues>0: repairs.append('Openstaande migratieproblemen vastgesteld.')
 if blockers or score<60: decision='ROLLBACK'
 elif repairs or score<85: decision='HERSTELLEN'
 else: decision='BEHOUDEN'
 status={'BEHOUDEN':'POST-ACTIVATION ASSURANCE GESLAAGD','HERSTELLEN':'POST-ACTIVATION HERSTEL VEREIST','ROLLBACK':'ROLLBACK BESLUIT VEREIST'}[decision]
 review_id=_id(cutover.get('cutover_id',''),cutover.get('new_version',''),score)
 return {'post_activation_assurance_rollback_control_version':ENGINE_VERSION,'review_id':review_id,'status':status,'decision':decision,'assurance_score':score,'active_version':cutover.get('new_version',''),'rollback_version':cutover.get('rollback_version',''),'compliance_score':compliance,'kpi_stability_score':kpi,'critical_incidents':incidents,'new_waivers':waivers,'migration_issues':migration_issues,'control_failures':control_failures,'rollback_blockers':blockers,'repair_items':repairs,'human_board_decision_required':decision in {'HERSTELLEN','ROLLBACK'},'human_legal_governance_review_required':decision=='ROLLBACK','automatic_rollback':False,'automatic_repair':False,'automatic_decision':False,'next_action':'Bevestig behoud van de actieve versie.' if decision=='BEHOUDEN' else ('Leg herstelmaatregelen, eigenaar en deadline vast.' if decision=='HERSTELLEN' else 'Laat Bestuur/ALV formeel besluiten over rollback naar de geregistreerde rollback-versie.')}
