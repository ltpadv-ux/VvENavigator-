"""Enterprise 11.5 Governance Archive & Institutional Memory.

Summarizes fully closed governance dossiers into a durable institutional memory
record with decision, rationale, costs, outcomes, evidence and lessons learned.
This archive supports continuity; it does not replace statutory records.
"""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='11.5.0'

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _id(*parts:Any)->str:
    return 'GOVMEM-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()

def build_governance_archive_memory(register:dict[str,Any], closure_result:dict[str,Any], alv_pack:dict[str,Any]|None=None, explainable:dict[str,Any]|None=None, learning:dict[str,Any]|None=None, context:dict[str,Any]|None=None, archive:dict[str,Any]|None=None)->dict[str,Any]:
    alv_pack=alv_pack or {}; explainable=explainable or {}; learning=learning or {}; context=context or {}; archive=archive or {}
    resolution=register.get('resolution',{}) or {}; mandate=register.get('execution_mandate',{}) or {}; closure=closure_result.get('closure',{}) or {}; discharge=closure_result.get('discharge',{}) or {}; pack=alv_pack.get('pack',{}) or {}; best=explainable.get('best_explanation',{}) or {}
    entries=list(archive.get('entries',[]) or [])
    if closure_result.get('status')!='SLUITING & DECHARGE GEREED' or not resolution or not closure:
        return {'governance_archive_memory_version':ENGINE_VERSION,'status':'DOSSIER NOG NIET ARCHIVEERBAAR','entry_count':len(entries),'entries':entries,'automatic_record_replacement':False}
    memory_id=_id(resolution.get('resolution_id',''),closure.get('closure_id',''),discharge.get('discharge_id',''))
    prior=next((x for x in entries if x.get('memory_id')==memory_id),{})
    planned=_num(closure.get('planned_budget',mandate.get('budget'))); actual=_num(closure.get('actual_spend'))
    lessons=context.get('lessons_learned',prior.get('lessons_learned',[])) or []
    if isinstance(lessons,str): lessons=[lessons]
    evidence=closure.get('evidence',[]) or []
    entry={
      'memory_id':memory_id,
      'resolution_id':resolution.get('resolution_id',''),
      'mandate_id':mandate.get('mandate_id',''),
      'closure_id':closure.get('closure_id',''),
      'discharge_id':discharge.get('discharge_id',''),
      'title':context.get('title',pack.get('title','Governance dossier')),
      'meeting_date':resolution.get('meeting_date',pack.get('meeting_date','')),
      'decision_authority':resolution.get('decision_authority',''),
      'decision_text':resolution.get('resolution_text',pack.get('proposal','')),
      'decision_rationale':context.get('decision_rationale',best.get('why_recommended',pack.get('why_this_option',''))),
      'financial_result':{'planned_budget':planned,'actual_spend':actual,'variance':round(actual-planned,2) if planned else 0.0},
      'delivery_note':closure.get('delivery_note',''),
      'final_result':closure.get('final_result',''),
      'evidence_count':len(evidence),
      'evidence':evidence,
      'lessons_learned':lessons,
      'what_worked':context.get('what_worked',prior.get('what_worked',[])),
      'what_to_improve':context.get('what_to_improve',prior.get('what_to_improve',[])),
      'future_recommendation':context.get('future_recommendation',prior.get('future_recommendation','')),
      'source_versions':{'closure':closure_result.get('resolution_closure_governance_discharge_version',''),'alv_pack':alv_pack.get('board_decision_alv_pack_version',''),'explainability':explainable.get('explainable_governance_ai_version',''),'learning_library':learning.get('preventive_learning_library_version','')},
      'minutes_reference':discharge.get('minutes_reference',resolution.get('minutes_reference','')),
      'archive_status':'GEARCHIVEERD',
      'statutory_records_still_required':True
    }
    entries=[x for x in entries if x.get('memory_id')!=memory_id]+[entry]
    entries.sort(key=lambda x:(str(x.get('meeting_date','')),str(x.get('memory_id',''))),reverse=True)
    return {'governance_archive_memory_version':ENGINE_VERSION,'status':'INSTITUTIONEEL GEHEUGEN BIJGEWERKT','entry_count':len(entries),'entries':entries,'latest_memory':entry,'human_archive_validation_required':True,'automatic_record_replacement':False,'automatic_legal_record_creation':False,'next_action':'Valideer de samenvatting en gebruik dit geheugen als context voor toekomstige bestuurs- en ALV-besluiten.'}
