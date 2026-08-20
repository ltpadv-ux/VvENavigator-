"""Enterprise 13.0 Constitutional Governance Control Tower."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='13.0.0'

def _id(*parts:Any)->str:return 'GOVTWR-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def build_control_tower(version:dict[str,Any]|None=None, gate:dict[str,Any]|None=None, debt:dict[str,Any]|None=None, amendments:dict[str,Any]|None=None, migration:dict[str,Any]|None=None, assurance:dict[str,Any]|None=None, waivers:dict[str,Any]|None=None)->dict[str,Any]:
 version=version or {}; gate=gate or {}; debt=debt or {}; amendments=amendments or {}; migration=migration or {}; assurance=assurance or {}; waivers=waivers or {}
 active_version=str((version.get('current_version') or {}).get('version',version.get('new_version',version.get('active_version',''))))
 compliance=_num(gate.get('compliance_score',100)); debt_score=_num(debt.get('constitutional_debt_score',0)); assurance_score=_num(assurance.get('assurance_score',100)); open_migrations=int(_num(migration.get('open_migration_count',0))); active_waivers=int(_num(debt.get('active_waivers',waivers.get('active_waivers',0)))); amendment_count=int(_num(amendments.get('action_count',len(amendments.get('actions',[]) or []))))
 assurance_decision=str(assurance.get('decision','BEHOUDEN')).upper(); gate_status=str(gate.get('gate','GO')).upper(); debt_level=str(debt.get('constitutional_debt_level','GROEN')).upper()
 alerts=[]
 if assurance_decision=='ROLLBACK': alerts.append({'priority':'KRITIEK','message':'Post-activation assurance adviseert ROLLBACK.'})
 if gate_status=='BLOCK': alerts.append({'priority':'KRITIEK','message':'Constitutionele decision gate staat op BLOCK.'})
 if debt_level=='ROOD': alerts.append({'priority':'KRITIEK','message':'Constitutionele schuld staat op ROOD.'})
 if open_migrations>0: alerts.append({'priority':'HOOG','message':f'{open_migrations} constitutionele migraties staan nog open.'})
 if active_waivers>0: alerts.append({'priority':'HOOG','message':f'{active_waivers} actieve waivers vereisen monitoring.'})
 if assurance_decision=='HERSTELLEN': alerts.append({'priority':'HOOG','message':'Post-activation assurance vereist herstelmaatregelen.'})
 health=round(max(0,min(100, compliance*0.30 + assurance_score*0.30 + max(0,100-debt_score)*0.25 + max(0,100-open_migrations*10)*0.10 + max(0,100-active_waivers*10)*0.05)),1)
 if any(a['priority']=='KRITIEK' for a in alerts): tower_status='DIRECT BESTUURLIJK BESLUIT VEREIST'
 elif alerts: tower_status='ACTIE VEREIST'
 else: tower_status='OP KOERS'
 return {'constitutional_governance_control_tower_version':ENGINE_VERSION,'tower_id':_id(active_version,gate_status,debt_level,assurance_decision),'status':tower_status,'constitutional_health_score':health,'active_constitution_version':active_version,'decision_gate':gate_status,'constitutional_compliance_score':compliance,'constitutional_debt_score':debt_score,'constitutional_debt_level':debt_level,'active_waivers':active_waivers,'open_migrations':open_migrations,'remediation_action_count':amendment_count,'post_activation_assurance_score':assurance_score,'assurance_decision':assurance_decision,'rollback_version':assurance.get('rollback_version',''),'alerts':alerts[:10],'human_board_decision_required':tower_status!='OP KOERS','automatic_decision':False,'automatic_execution':False,'automatic_rollback':False,'single_source_of_truth':True,'next_action':'Behandel kritieke governance-signalen eerst.' if tower_status=='DIRECT BESTUURLIJK BESLUIT VEREIST' else ('Werk openstaande governance-acties af.' if tower_status=='ACTIE VEREIST' else 'Blijf periodiek monitoren.')}
