"""Enterprise 12.2 Constitutional Exception & Waiver Register."""
from __future__ import annotations
from datetime import date, datetime
from hashlib import sha256
from typing import Any
ENGINE_VERSION='12.2.0'
APPROVED={'GOEDGEKEURD','VASTGESTELD','APPROVED','VERLEEND'}

def _id(*parts:Any)->str:return 'GOVWVR-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0
def _date(v:Any):
 if not v:return None
 try:return datetime.fromisoformat(str(v)).date()
 except Exception:return None

def register_constitutional_waiver(gate:dict[str,Any], proposal:dict[str,Any], waiver:dict[str,Any]|None=None, today:date|None=None, existing:dict[str,Any]|None=None)->dict[str,Any]:
 waiver=waiver or {}; existing=existing or {}; today=today or date.today()
 gate_status=str(gate.get('gate','')).upper()
 if gate_status=='GO':
  return {'constitutional_exception_waiver_register_version':ENGINE_VERSION,'status':'GEEN WAIVER NODIG','waiver':{},'automatic_approval':False}
 reason=str(waiver.get('reason',existing.get('reason',''))).strip()
 authority=str(waiver.get('decision_authority',existing.get('decision_authority',''))).strip()
 approval=str(waiver.get('approval_status',existing.get('approval_status','CONCEPT'))).upper()
 valid_from=_date(waiver.get('valid_from',existing.get('valid_from',str(today))))
 valid_until=_date(waiver.get('valid_until',existing.get('valid_until')))
 review_date=_date(waiver.get('review_date',existing.get('review_date')))
 financial_impact=_num(waiver.get('financial_impact_eur',existing.get('financial_impact_eur',proposal.get('financial_commitment_eur',0))))
 risk_acceptance=str(waiver.get('risk_acceptance',existing.get('risk_acceptance',''))).strip()
 scope=str(waiver.get('scope',existing.get('scope',proposal.get('proposal_id','')))).strip()
 temporary=bool(valid_until)
 complete=all([reason,authority,scope,valid_from,review_date,risk_acceptance])
 approved=approval in APPROVED and complete
 expired=bool(valid_until and today>valid_until)
 review_due=bool(review_date and today>=review_date)
 waiver_id=existing.get('waiver_id') or _id(gate.get('gate_id',''),proposal.get('proposal_id',''),reason)
 record={'waiver_id':waiver_id,'gate_id':gate.get('gate_id',''),'proposal_id':proposal.get('proposal_id',''),'scope':scope,'reason':reason,'decision_authority':authority,'approval_status':approval,'valid_from':str(valid_from) if valid_from else '','valid_until':str(valid_until) if valid_until else '','review_date':str(review_date) if review_date else '','financial_impact_eur':financial_impact,'risk_acceptance':risk_acceptance,'temporary':temporary,'expired':expired,'review_due':review_due,'source_gate':gate_status,'source_blockers':gate.get('blockers',[]),'source_review_items':gate.get('review_items',[]),'human_approval_required':True}
 status='WAIVER ACTIEF' if approved and not expired else ('WAIVER VERLOPEN' if expired else ('WAIVER REVIEW VEREIST' if review_due and approved else 'WAIVER ONVOLLEDIG OF NIET GOEDGEKEURD'))
 return {'constitutional_exception_waiver_register_version':ENGINE_VERSION,'status':status,'waiver':record,'human_legal_governance_review_required':True,'automatic_approval':False,'automatic_policy_change':False,'automatic_decision':False,'automatic_execution':False,'next_action':'Herbeoordeel waiver vóór vervaldatum of reviewdatum.' if approved else 'Vul reden, bevoegd orgaan, risicoacceptatie, geldigheid en reviewdatum aan en laat formeel goedkeuren.'}
