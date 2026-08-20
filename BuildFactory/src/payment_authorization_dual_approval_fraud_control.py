"""Enterprise 14.6 Payment Authorization, Dual Approval & Fraud Signal Control."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='14.6.0'

def _id(*parts:Any)->str:return 'GOVPAY-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def authorize_payment(three_way:dict[str,Any], payment:dict[str,Any], vendor:dict[str,Any], history:list[dict[str,Any]]|None=None, rules:dict[str,Any]|None=None)->dict[str,Any]:
 history=history or []; rules=rules or {}
 matched=bool(three_way.get('payment_workflow_approved',False) or three_way.get('three_way_match_passed',False) or str(three_way.get('status','')).upper()=='THREE-WAY MATCH GESLAAGD')
 invoice_no=str(payment.get('invoice_number','')).strip(); supplier=str(payment.get('supplier_id',vendor.get('supplier_id',''))).strip(); iban=str(payment.get('iban','')).replace(' ','').upper(); expected_iban=str(vendor.get('verified_iban','')).replace(' ','').upper(); amount=_num(payment.get('amount_eur',three_way.get('invoice_amount_eur',0)))
 approvers=[str(x).strip() for x in payment.get('approvers',[]) if str(x).strip()]; distinct_approvers=len(set(approvers)); dual_ok=distinct_approvers>=2
 iban_ok=bool(iban and expected_iban and iban==expected_iban); supplier_ok=bool(supplier and supplier==str(vendor.get('supplier_id','')).strip())
 duplicate=any(str(x.get('invoice_number','')).strip()==invoice_no and str(x.get('supplier_id','')).strip()==supplier for x in history)
 unusual_threshold=_num(rules.get('unusual_amount_eur',50000)); unusual_amount=amount>=unusual_threshold if unusual_threshold>0 else False
 bank_change=bool(vendor.get('iban_changed_recently',False)); vendor_change=bool(vendor.get('master_data_changed_recently',False))
 blockers=[]; warnings=[]
 if not matched:blockers.append('Three-way match is niet succesvol afgerond.')
 if not dual_ok:blockers.append('Dubbele autorisatie door twee verschillende bevoegde personen ontbreekt.')
 if not supplier_ok:blockers.append('Leveranciersidentiteit komt niet overeen met de gevalideerde leverancier.')
 if not iban_ok:blockers.append('IBAN komt niet overeen met het geverifieerde leveranciers-IBAN.')
 if duplicate:blockers.append('Mogelijke dubbele factuur gedetecteerd.')
 if amount<=0:blockers.append('Betaalbedrag ontbreekt of is ongeldig.')
 if unusual_amount:warnings.append('Ongebruikelijk hoog betaalbedrag: aanvullende review vereist.')
 if bank_change:warnings.append('Leveranciers-IBAN is recent gewijzigd.')
 if vendor_change:warnings.append('Leveranciersmasterdata is recent gewijzigd.')
 fraud_score=min(100,(40 if duplicate else 0)+(25 if not iban_ok else 0)+(15 if bank_change else 0)+(10 if vendor_change else 0)+(10 if unusual_amount else 0))
 ready=not blockers and fraud_score<50
 status='BETALING GEREED VOOR HANDMATIGE VRIJGAVE' if ready else ('BETALING REVIEW VEREIST' if not blockers else 'BETALING GEBLOKKEERD')
 return {'payment_authorization_dual_approval_fraud_control_version':ENGINE_VERSION,'payment_control_id':_id(three_way.get('three_way_id',''),invoice_no,supplier,amount),'status':status,'payment_amount_eur':round(amount,2),'supplier_id':supplier,'invoice_number':invoice_no,'dual_approval_ok':dual_ok,'distinct_approver_count':distinct_approvers,'supplier_identity_ok':supplier_ok,'iban_match_ok':iban_ok,'duplicate_invoice_detected':duplicate,'unusual_amount_detected':unusual_amount,'recent_iban_change':bank_change,'recent_vendor_master_change':vendor_change,'fraud_signal_score':fraud_score,'blockers':blockers,'warnings':warnings,'ready_for_manual_release':ready,'human_payment_release_required':True,'human_treasurer_confirmation_required':True,'automatic_payment':False,'automatic_batch_release':False,'automatic_vendor_change':False,'next_action':'Laat twee bevoegde personen de betaling handmatig vrijgeven na controle van fraud-signalen.' if ready else 'Los blockers op en laat waarschuwingen expliciet beoordelen vóór vrijgave.'}
