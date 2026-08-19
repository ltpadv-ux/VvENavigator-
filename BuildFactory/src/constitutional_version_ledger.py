"""Enterprise 12.6 Controlled Amendment Application & Constitutional Version Ledger."""
from __future__ import annotations
from copy import deepcopy
from hashlib import sha256
from typing import Any
ENGINE_VERSION='12.6.0'

def _id(prefix:str,*parts:Any)->str:return f"{prefix}-"+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()

def apply_approved_amendment(amendment_result:dict[str,Any], current:dict[str,Any], ledger:dict[str,Any]|None=None)->dict[str,Any]:
 ledger=deepcopy(ledger or {'versions':[]}); amendment=amendment_result.get('amendment',{}) or {}
 if not amendment_result.get('ready_for_controlled_processing',False):
  return {'constitutional_version_ledger_version':ENGINE_VERSION,'status':'AMENDMENT NIET TOEPASBAAR','current_version':current,'ledger':ledger,'automatic_application':False}
 target=amendment.get('target'); new=deepcopy(current)
 version_from=str(amendment.get('version_from') or current.get('version') or '1.0'); version_to=str(amendment.get('version_to') or '').strip()
 if not version_to:
  return {'constitutional_version_ledger_version':ENGINE_VERSION,'status':'DOELVERSIE ONTBREEKT','current_version':current,'ledger':ledger,'automatic_application':False}
 snapshot={'version_id':_id('GOVVER',version_from,current.get('constitution_id',''),amendment.get('amendment_id','')),'version':version_from,'constitution_id':current.get('constitution_id',''),'content':deepcopy(current),'immutable':True,'superseded_by':version_to,'source_amendment_id':amendment.get('amendment_id','')}
 if not any(v.get('version_id')==snapshot['version_id'] for v in ledger.get('versions',[])): ledger.setdefault('versions',[]).append(snapshot)
 new['version']=version_to; new['previous_version']=version_from; new['source_amendment_id']=amendment.get('amendment_id'); new['effective_date']=amendment.get('effective_date'); new['review_date']=amendment.get('review_date')
 if target=='GOVERNANCE_CONSTITUTION':
  new['constitution_id']=_id('GOVCONST',version_to,amendment.get('resolution_reference',''))
 elif target=='STRATEGIC_DOCTRINE':
  new['doctrine_version']=version_to
 elif target=='WAIVER_REGISTER':
  new['waiver_register_version']=version_to
 new['amendment_history']=list(new.get('amendment_history',[]))+[{'amendment_id':amendment.get('amendment_id'),'target':target,'version_from':version_from,'version_to':version_to,'resolution_reference':amendment.get('resolution_reference'),'rationale':amendment.get('rationale')}]
 ledger['active_version']=version_to; ledger['active_target']=target; ledger['last_amendment_id']=amendment.get('amendment_id')
 return {'constitutional_version_ledger_version':ENGINE_VERSION,'status':'AMENDMENT GECONTROLEERD VERWERKT','applied_target':target,'previous_version':version_from,'new_version':version_to,'current_version':new,'ledger':ledger,'historical_versions_preserved':True,'human_validation_required':True,'automatic_application':False,'automatic_policy_change':False,'automatic_decision':False}
