"""Enterprise 14.7 Payment Reconciliation & Bank Statement Control."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='14.7.0'

def _id(*parts:Any)->str:return 'GOVREC-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def reconcile_payment(payment_control:dict[str,Any], bank:dict[str,Any], ledger:dict[str,Any], history:list[dict[str,Any]]|None=None, tolerance_eur:float=0.01)->dict[str,Any]:
 history=history or []; ready=bool(payment_control.get('ready_for_manual_release',False) or str(payment_control.get('status','')).upper()=='BETALING GEREED VOOR HANDMATIGE VRIJGAVE')
 expected=_num(payment_control.get('payment_amount_eur',0)); bank_amount=_num(bank.get('amount_eur',0)); ledger_amount=_num(ledger.get('payment_amount_eur',ledger.get('amount_eur',0))); supplier=str(payment_control.get('supplier_id','')); bank_supplier=str(bank.get('supplier_id','')); inv=str(payment_control.get('invoice_number','')); bank_inv=str(bank.get('invoice_number','')); iban=str(bank.get('iban','')).replace(' ','').upper(); expected_iban=str(bank.get('expected_iban',iban)).replace(' ','').upper()
 amount_match=abs(bank_amount-expected)<=tolerance_eur and abs(ledger_amount-expected)<=tolerance_eur
 supplier_match=bool(supplier and bank_supplier and supplier==bank_supplier)
 invoice_match=bool(inv and bank_inv and inv==bank_inv)
 iban_match=bool(iban and expected_iban and iban==expected_iban)
 reversed_tx=bool(bank.get('reversed',False) or bank.get('storno',False))
 duplicate_payment=any(str(x.get('invoice_number',''))==inv and str(x.get('supplier_id',''))==supplier and abs(_num(x.get('amount_eur',0))-bank_amount)<=tolerance_eur for x in history)
 blockers=[]; warnings=[]
 if not ready:blockers.append('Betaling was niet gereed voor handmatige vrijgave.')
 if not amount_match:blockers.append('Bankmutatie, betaalopdracht en ledgerbedrag sluiten niet aan.')
 if not supplier_match:blockers.append('Leverancier op bankmutatie wijkt af van betaalopdracht.')
 if not invoice_match:blockers.append('Factuurreferentie op bankmutatie wijkt af.')
 if not iban_match:blockers.append('IBAN op bankmutatie wijkt af van verwachte rekening.')
 if reversed_tx:warnings.append('Stornering/terugboeking gedetecteerd.')
 if duplicate_payment:blockers.append('Mogelijke dubbele betaling gedetecteerd.')
 reconciled=not blockers and not reversed_tx
 status='BETALING VOLLEDIG GERECONCILIEERD' if reconciled else ('RECONCILIATIE REVIEW VEREIST' if not blockers else 'RECONCILIATIE GEBLOKKEERD')
 return {'payment_reconciliation_bank_statement_control_version':ENGINE_VERSION,'reconciliation_id':_id(payment_control.get('payment_control_id',''),bank.get('transaction_id',''),inv,bank_amount),'status':status,'expected_payment_eur':round(expected,2),'bank_amount_eur':round(bank_amount,2),'ledger_amount_eur':round(ledger_amount,2),'amount_match':amount_match,'supplier_match':supplier_match,'invoice_reference_match':invoice_match,'iban_match':iban_match,'reversal_detected':reversed_tx,'duplicate_payment_detected':duplicate_payment,'blockers':blockers,'warnings':warnings,'reconciled':reconciled,'human_finance_review_required':not reconciled,'automatic_ledger_posting':False,'automatic_reversal_handling':False,'automatic_payment':False,'next_action':'Markeer betaling als financieel afgeletterd en neem op in audittrail.' if reconciled else 'Onderzoek verschillen, storneringen of dubbele betaling en herstel de aansluiting.'}
