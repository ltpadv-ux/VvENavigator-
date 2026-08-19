"""Enterprise 11.2 Formal Resolution & Voting Register.

Transforms an ALV decision pack into a formal, traceable resolution record with
quorum, votes, authority, minutes reference and execution mandate. The engine
records governance facts; it does not create legal validity by itself.
"""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='11.2.0'
APPROVED={'AANGENOMEN','GOEDGEKEURD','AKKOORD','APPROVED'}
REJECTED={'VERWORPEN','AFGEWEZEN','REJECTED'}

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _id(prefix:str,*parts:Any)->str:
    return f"{prefix}-"+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()

def build_formal_resolution_voting_register(alv_pack:dict[str,Any], voting:dict[str,Any]|None=None, existing:dict[str,Any]|None=None)->dict[str,Any]:
    voting=voting or {}; existing=existing or {}; pack=alv_pack.get('pack',{}) or {}
    if alv_pack.get('status')!='BESLUITSTUK GEREED' or not pack:
        return {'formal_resolution_voting_register_version':ENGINE_VERSION,'status':'GEEN BESLUITSTUK','resolution':{},'execution_mandate':{},'automatic_execution':False}
    pack_id=pack.get('pack_id','')
    prior=existing.get('resolution',{}) or {}
    present=_num(voting.get('present_votes',prior.get('present_votes',0)))
    total=_num(voting.get('eligible_votes',prior.get('eligible_votes',0)))
    quorum_required=_num(voting.get('quorum_required_pct',prior.get('quorum_required_pct',50)))
    quorum_pct=round((present/total*100),1) if total>0 else 0.0
    quorum_met=bool(total>0 and quorum_pct>=quorum_required)
    for_votes=_num(voting.get('votes_for',prior.get('votes_for',0)))
    against=_num(voting.get('votes_against',prior.get('votes_against',0)))
    abstain=_num(voting.get('abstentions',prior.get('abstentions',0)))
    cast=for_votes+against
    majority_required=_num(voting.get('majority_required_pct',prior.get('majority_required_pct',50)))
    approval_pct=round((for_votes/cast*100),1) if cast>0 else 0.0
    majority_met=bool(cast>0 and approval_pct>majority_required)
    recorded=str(voting.get('decision_status',prior.get('decision_status',''))).upper()
    if not recorded:
        recorded='AANGENOMEN' if quorum_met and majority_met else ('VERWORPEN' if quorum_met and cast>0 else 'STEMMING ONVOLLEDIG')
    resolution_id=prior.get('resolution_id') or _id('ALVRES',pack_id,pack.get('meeting_date',''),pack.get('proposal',''))
    authority=str(voting.get('decision_authority',prior.get('decision_authority',pack.get('meeting_type','Bestuur/ALV'))))
    minutes_reference=str(voting.get('minutes_reference',prior.get('minutes_reference','')))
    decision_text=str(voting.get('resolution_text',prior.get('resolution_text',pack.get('proposal',''))))
    formal_complete=all([pack_id,decision_text,authority,minutes_reference,total>0,present>0])
    adopted=recorded in APPROVED and quorum_met and majority_met and formal_complete
    resolution={
      'resolution_id':resolution_id,'pack_id':pack_id,'meeting_type':pack.get('meeting_type','Bestuur/ALV'),'meeting_date':pack.get('meeting_date',''),
      'decision_authority':authority,'resolution_text':decision_text,'minutes_reference':minutes_reference,'decision_status':recorded,
      'eligible_votes':total,'present_votes':present,'quorum_required_pct':quorum_required,'quorum_pct':quorum_pct,'quorum_met':quorum_met,
      'votes_for':for_votes,'votes_against':against,'abstentions':abstain,'majority_required_pct':majority_required,'approval_pct':approval_pct,'majority_met':majority_met,
      'formal_record_complete':formal_complete,'adopted':adopted,'chair':voting.get('chair',prior.get('chair','')),'secretary':voting.get('secretary',prior.get('secretary','')),
      'attachments':voting.get('attachments',prior.get('attachments',[])),'legal_validity_requires_human_check':True
    }
    mandate={}
    if adopted:
        old=existing.get('execution_mandate',{}) or {}
        mandate_id=old.get('mandate_id') or _id('ALVMND',resolution_id,decision_text)
        mandate={'mandate_id':mandate_id,'resolution_id':resolution_id,'status':'UITVOERINGSMANDAAT ACTIEF','owner':old.get('owner',voting.get('owner','Bestuur')),'budget':old.get('budget',voting.get('budget',pack.get('financial_impact'))),'deadline':old.get('deadline',voting.get('deadline','')),'kpi_targets':old.get('kpi_targets',voting.get('kpi_targets',pack.get('expected_effect',{}))),'evidence_required':True,'progress_pct':old.get('progress_pct',0),'actual_spend':old.get('actual_spend',0),'evidence':old.get('evidence',[])}
    status='BESLUIT AANGENOMEN - MANDAAT GEREED' if adopted else ('FORMELE REGISTRATIE ONVOLLEDIG' if not formal_complete else ('QUORUM NIET GEHAALD' if not quorum_met else ('BESLUIT VERWORPEN' if recorded in REJECTED or not majority_met else 'BESLUITSTATUS CONTROLEREN')))
    return {'formal_resolution_voting_register_version':ENGINE_VERSION,'status':status,'resolution':resolution,'execution_mandate':mandate,'human_legal_validation_required':True,'automatic_legal_opinion':False,'automatic_execution':False,'automatic_budget_commitment':False,'next_action':'Valideer besluit, bevoegdheid, quorum en notulen; activeer uitvoering alleen na menselijke bevestiging.' if adopted else 'Maak de formele besluitregistratie compleet of behandel het voorstel opnieuw volgens de geldende VvE-regels.'}
