"""Enterprise 14.2 ALV Voting, Quorum & Financial Resolution Validation Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='14.2.0'

def _id(*parts:Any)->str:return 'GOVVLD-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def validate_financial_resolution(pack:dict[str,Any], vote:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; total=_num(vote.get('total_vote_weight')); present=_num(vote.get('present_vote_weight')); yes=_num(vote.get('yes_vote_weight')); no=_num(vote.get('no_vote_weight')); abstain=_num(vote.get('abstain_vote_weight'))
 quorum_req=_num(rules.get('quorum_pct',vote.get('required_quorum_pct',50))); majority_req=_num(rules.get('majority_pct',vote.get('required_majority_pct',50)))
 quorum_pct=round(present/total*100,2) if total>0 else 0; cast=yes+no; yes_pct=round(yes/cast*100,2) if cast>0 else 0
 quorum_ok=quorum_pct>=quorum_req; majority_ok=yes_pct>majority_req if bool(rules.get('strictly_greater_majority',True)) else yes_pct>=majority_req
 text_ok=bool(str(pack.get('draft_alv_resolution','')).strip()); pack_ok=pack.get('recommendation')!='NIET VOORLEGGEN ZONDER HERIJKING'; mandate_ok=bool(vote.get('financial_mandate_confirmed',False)); minutes_ok=bool(vote.get('minutes_record_complete',False))
 blockers=[]
 if not quorum_ok:blockers.append('Vereist quorum is niet gehaald.')
 if not majority_ok:blockers.append('Vereiste meerderheid is niet gehaald.')
 if not text_ok:blockers.append('Definitieve besluittekst ontbreekt.')
 if not pack_ok:blockers.append('Financieel besluitpakket bevat een herijkingsblokkade.')
 if not mandate_ok:blockers.append('Financieel mandaat is niet bevestigd.')
 if not minutes_ok:blockers.append('Stemuitslag/notulenregistratie is nog niet compleet.')
 adopted=not blockers
 return {'alv_voting_quorum_financial_resolution_validation_version':ENGINE_VERSION,'validation_id':_id(pack.get('resolution_pack_id',''),vote.get('meeting_id',''),yes,no,abstain),'status':'BESLUIT VALIDATIE GESLAAGD' if adopted else 'BESLUIT NIET GEREED VOOR VASTSTELLING','quorum_pct':quorum_pct,'required_quorum_pct':quorum_req,'quorum_ok':quorum_ok,'yes_pct_excluding_abstentions':yes_pct,'required_majority_pct':majority_req,'majority_ok':majority_ok,'vote_weights':{'total':total,'present':present,'yes':yes,'no':no,'abstain':abstain},'resolution_text_present':text_ok,'financial_pack_clear':pack_ok,'financial_mandate_confirmed':mandate_ok,'minutes_record_complete':minutes_ok,'blockers':blockers,'validated_for_formal_registration':adopted,'human_chair_confirmation_required':True,'human_legal_governance_review_required':True,'automatic_adoption':False,'automatic_execution':False,'next_action':'Laat voorzitter/stemcommissie de uitslag bevestigen en registreer daarna het formele besluit.' if adopted else 'Los de validatieblokkades op of behandel het voorstel opnieuw volgens statuten/reglement.'}
