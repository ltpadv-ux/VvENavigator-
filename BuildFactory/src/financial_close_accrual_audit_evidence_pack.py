"""Enterprise 14.8 Financial Close, Accrual & Audit Evidence Pack."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='14.8.0'
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0
def _id(*p:Any)->str:return 'GOVCLS-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def build_financial_close(period:str, ledger:list[dict[str,Any]], invoices:list[dict[str,Any]], reconciliations:list[dict[str,Any]], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; tol=_num(rules.get('close_tolerance_eur',0.01)); committed=sum(_num(x.get('amount_eur')) for x in ledger if str(x.get('entry_type','')).upper() in {'COMMITMENT','CONTRACT','ORDER'}); spent=sum(_num(x.get('amount_eur')) for x in ledger if str(x.get('entry_type','')).upper() in {'SPEND','PAYMENT'}); invoiced=sum(_num(x.get('amount_eur')) for x in invoices); paid=sum(_num(x.get('amount_eur')) for x in invoices if x.get('paid',False)); accrual=max(0.0,committed-invoiced); payable=max(0.0,invoiced-paid)
 unreconciled=[x for x in reconciliations if not x.get('audit_ready',False) and str(x.get('status','')).upper()!='BETALING VOLLEDIG GERECONCILIEERD']; evidence_missing=[x for x in invoices if not x.get('invoice_number') or not x.get('supplier_id')]; variance=round(spent-paid,2); blockers=[]
 if unreconciled:blockers.append('Niet alle betalingen zijn volledig gereconcilieerd.')
 if evidence_missing:blockers.append('Factuur-/leveranciersbewijs is onvolledig.')
 if abs(variance)>tol:blockers.append('Ledgerbetalingen en betaalde facturen sluiten niet aan binnen tolerantie.')
 ready=not blockers
 return {'financial_close_accrual_audit_evidence_pack_version':ENGINE_VERSION,'close_id':_id(period,committed,invoiced,paid),'period':period,'status':'PERIODE AFSLUITING AUDIT-READY' if ready else 'PERIODE AFSLUITING REVIEW VEREIST','committed_eur':round(committed,2),'invoiced_eur':round(invoiced,2),'paid_eur':round(paid,2),'spent_ledger_eur':round(spent,2),'accrual_eur':round(accrual,2),'accounts_payable_eur':round(payable,2),'ledger_payment_variance_eur':variance,'unreconciled_payment_count':len(unreconciled),'missing_evidence_count':len(evidence_missing),'blockers':blockers,'audit_evidence_pack':{'ledger_entries':len(ledger),'invoices':len(invoices),'reconciliations':len(reconciliations),'evidence_complete':not evidence_missing,'reconciliation_complete':not unreconciled},'audit_ready':ready,'human_financial_close_approval_required':True,'human_auditor_review_required':True,'automatic_journal_posting':False,'automatic_close':False,'automatic_payment':False,'next_action':'Laat financieel verantwoordelijke en auditor de afsluiting en bewijsset beoordelen.' if ready else 'Los afsluitingsverschillen en ontbrekend auditbewijs op vóór formele periodeafsluiting.'}
