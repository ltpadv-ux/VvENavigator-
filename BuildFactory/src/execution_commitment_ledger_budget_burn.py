"""Enterprise 14.4 Execution Commitment Ledger & Budget Burn Control."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='14.4.0'

def _id(*parts:Any)->str:return 'GOVLED-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def build_commitment_ledger(mandate:dict[str,Any], entries:list[dict[str,Any]]|None=None)->dict[str,Any]:
 entries=entries or []; maximum=_num(mandate.get('maximum_commitment_eur',0)); active=bool(mandate.get('budget_lock_active',False))
 rows=[]; reserved=committed=spent=0.0; blockers=[]
 for e in entries:
  typ=str(e.get('type','')).upper(); amount=max(0,_num(e.get('amount_eur',0))); status=str(e.get('status','OPEN')).upper(); ref=str(e.get('reference','')).strip()
  if typ=='RESERVATION': reserved+=amount
  elif typ in {'COMMITMENT','CONTRACT','ORDER'}: committed+=amount
  elif typ in {'SPEND','INVOICE','PAYMENT'}: spent+=amount
  else: blockers.append(f"Onbekend entry type: {typ or 'LEEG'}")
  rows.append({'entry_id':e.get('entry_id') or _id(mandate.get('mandate_id',''),typ,ref,amount),'type':typ,'reference':ref,'amount_eur':round(amount,2),'status':status,'owner':e.get('owner',''),'date':e.get('date','')})
 encumbered=max(committed,spent); used=max(reserved,encumbered); available=round(maximum-used,2); free=round(maximum-reserved,2); burn_pct=round((used/maximum*100),1) if maximum>0 else 0.0
 if not active:blockers.append('Budget-lock is niet actief.')
 if maximum<=0:blockers.append('Maximum commitment ontbreekt.')
 if reserved>maximum:blockers.append('Reserveringen overschrijden het mandaat.')
 if encumbered>maximum:blockers.append('Gecommitteerd/besteed bedrag overschrijdt het mandaat.')
 if spent>committed and committed>0:blockers.append('Besteed bedrag is hoger dan geregistreerde commitments.')
 status='BUDGET BURN BINNEN MANDAAT' if not blockers and used<=maximum else 'BUDGET BURN BLOKKADE / REVIEW VEREIST'
 return {'execution_commitment_ledger_budget_burn_version':ENGINE_VERSION,'ledger_id':_id(mandate.get('mandate_id',''),len(rows),maximum),'status':status,'mandate_id':mandate.get('mandate_id'),'maximum_commitment_eur':round(maximum,2),'reserved_eur':round(reserved,2),'committed_eur':round(committed,2),'spent_eur':round(spent,2),'free_eur':free,'available_after_commitments_eur':available,'budget_burn_pct':burn_pct,'entries':rows,'blockers':blockers,'budget_lock_active':active,'human_budget_owner_review_required':bool(blockers or burn_pct>=80),'automatic_spend':False,'automatic_commitment':False,'automatic_payment':False,'automatic_execution':False,'next_action':'Review resterend budget en bevestig iedere nieuwe verplichting tegen het actuele ledger.' if not blockers else 'Los ledger- of budgetblokkades op voordat nieuwe verplichtingen worden aangegaan.'}

def assess_new_ledger_entry(ledger:dict[str,Any], entry:dict[str,Any])->dict[str,Any]:
 amount=max(0,_num(entry.get('amount_eur',0))); maximum=_num(ledger.get('maximum_commitment_eur',0)); used=max(_num(ledger.get('reserved_eur',0)),_num(ledger.get('committed_eur',0)),_num(ledger.get('spent_eur',0))); projected=round(used+amount,2); allowed=bool(ledger.get('budget_lock_active',False)) and projected<=maximum and not ledger.get('blockers')
 return {'ledger_id':ledger.get('ledger_id'),'entry_type':entry.get('type'),'entry_amount_eur':round(amount,2),'used_before_eur':round(used,2),'projected_used_eur':projected,'maximum_commitment_eur':round(maximum,2),'allowed':allowed,'status':'ENTRY TOEGESTAAN' if allowed else 'ENTRY GEBLOKKEERD','automatic_posting':False}
