"""Enterprise 15.7 ALV Scenario Vote Validation & Activation Mandate Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='15.7.0'

def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def _id(*p:Any)->str:return 'GOVSAM-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()

def validate_vote_and_issue_activation_mandate(pack:dict[str,Any], vote:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; total=_n(vote.get('total_vote_weight')); present=_n(vote.get('present_vote_weight')); yes=_n(vote.get('yes_vote_weight')); no=_n(vote.get('no_vote_weight')); abstain=_n(vote.get('abstain_vote_weight'))
 quorum_req=_n(rules.get('quorum_pct',vote.get('required_quorum_pct',50))); majority_req=_n(rules.get('majority_pct',vote.get('required_majority_pct',50))); strict=bool(rules.get('strictly_greater_majority',True))
 quorum_pct=round(present/total*100,2) if total>0 else 0.0; cast=yes+no; yes_pct=round(yes/cast*100,2) if cast>0 else 0.0; quorum_ok=quorum_pct>=quorum_req; majority_ok=yes_pct>majority_req if strict else yes_pct>=majority_req
 pack_ready=str(pack.get('status','')).upper().startswith('CONFIDENCE-GATED BESLUITPAKKET GEREED'); text_ok=bool(str(vote.get('final_resolution_text',pack.get('draft_alv_resolution',''))).strip()); risk_limits_ok=bool(pack.get('risk_appetite_limits_pct')); confidence_ok=_n(pack.get('simulation_confidence_pct'))>0; minutes_ok=bool(vote.get('minutes_record_complete',False)); chair_ok=bool(vote.get('chair_confirmed',False)); execution_owner=str(vote.get('execution_owner','')).strip(); activation_date=str(vote.get('activation_date','')).strip()
 blockers=[]
 if not pack_ready:blockers.append('Confidence-gated besluitpakket is niet gereed.')
 if not quorum_ok:blockers.append('Vereist quorum is niet gehaald.')
 if not majority_ok:blockers.append('Vereiste meerderheid is niet gehaald.')
 if not text_ok:blockers.append('Definitieve ALV-besluittekst ontbreekt.')
 if not risk_limits_ok:blockers.append('Vastgestelde risicokaders ontbreken.')
 if not confidence_ok:blockers.append('Monte Carlo/confidence-bewijs ontbreekt.')
 if not minutes_ok:blockers.append('Stemuitslag/notulenregistratie is niet compleet.')
 if not chair_ok:blockers.append('Voorzittersbevestiging ontbreekt.')
 if not execution_owner:blockers.append('Uitvoeringsverantwoordelijke ontbreekt.')
 if not activation_date:blockers.append('Activatiedatum ontbreekt.')
 valid=not blockers
 mandate={'mandate_id':_id(pack.get('scenario_resolution_pack_id',''),vote.get('meeting_id',''),activation_date),'scenario_name':pack.get('scenario_name'),'activation_date':activation_date,'execution_owner':execution_owner,'risk_appetite_limits_pct':pack.get('risk_appetite_limits_pct'),'verified_shortfall_pct':pack.get('verified_shortfall_pct'),'simulation_confidence_pct':pack.get('simulation_confidence_pct'),'scope':'Uitvoering uitsluitend binnen het door de ALV vastgestelde scenario, budget, risicokaders en bestaande governance-controls.','active':False,'requires_manual_activation':True} if valid else None
 return {'alv_scenario_vote_validation_activation_mandate_version':ENGINE_VERSION,'vote_validation_id':_id(pack.get('scenario_resolution_pack_id',''),vote.get('meeting_id',''),yes,no,abstain),'status':'SCENARIOBESLUIT GEVALUEERD - ACTIVATIEMANDAAT GEREED' if valid else 'SCENARIOBESLUIT NIET GEREED VOOR ACTIVATIEMANDAAT','quorum_pct':quorum_pct,'required_quorum_pct':quorum_req,'quorum_ok':quorum_ok,'yes_pct_excluding_abstentions':yes_pct,'required_majority_pct':majority_req,'majority_ok':majority_ok,'vote_weights':{'total':total,'present':present,'yes':yes,'no':no,'abstain':abstain},'resolution_text_present':text_ok,'risk_framework_present':risk_limits_ok,'confidence_evidence_present':confidence_ok,'minutes_record_complete':minutes_ok,'chair_confirmed':chair_ok,'blockers':blockers,'activation_mandate':mandate,'validated_for_manual_activation':valid,'human_chair_confirmation_required':True,'human_board_activation_required':True,'human_legal_governance_review_required':True,'automatic_scenario_activation':False,'automatic_execution':False,'automatic_contribution_change':False,'automatic_reserve_change':False,'automatic_mjop_change':False,'next_action':'Registreer het formele ALV-besluit en activeer het scenario daarna handmatig binnen het mandaat.' if valid else 'Los de stem-, documentatie- of governanceblokkades op voordat een activatiemandaat wordt uitgegeven.'}
