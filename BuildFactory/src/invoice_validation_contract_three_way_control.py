"""Enterprise 14.5 Invoice Validation, Contract Match & Three-Way Control."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='14.5.0'

def _id(*parts:Any)->str:return 'GOV3WY-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def validate_invoice_three_way(mandate:dict[str,Any], contract:dict[str,Any], delivery:dict[str,Any], invoice:dict[str,Any], tolerance_pct:float=2.0)->dict[str,Any]:
 amount=max(0,_num(invoice.get('amount_eur'))); contract_amount=max(0,_num(contract.get('contract_amount_eur'))); delivered_value=max(0,_num(delivery.get('accepted_value_eur'))); tolerance=max(0,_num(tolerance_pct))/100
 mandate_active=bool(mandate.get('budget_lock_active',False)); max_commit=_num(mandate.get('maximum_commitment_eur',0)); contract_ref=str(invoice.get('contract_reference','')).strip(); expected_ref=str(contract.get('contract_reference','')).strip(); scope_ok=str(invoice.get('scope','')).strip()==str(contract.get('scope','')).strip() if contract.get('scope') else True
 period_ok=True
 if contract.get('period') and invoice.get('period'):period_ok=str(contract.get('period'))==str(invoice.get('period'))
 ref_ok=bool(expected_ref and contract_ref==expected_ref)
 contract_limit_ok=amount<=contract_amount*(1+tolerance) if contract_amount>0 else False
 delivery_ok=bool(delivery.get('accepted',False)) and amount<=delivered_value*(1+tolerance) if delivered_value>0 else bool(delivery.get('accepted',False))
 mandate_ok=mandate_active and amount<=max_commit
 change_order=bool(invoice.get('change_order',False)); change_approved=bool(invoice.get('change_order_approved',False))
 blockers=[]; reviews=[]
 if not mandate_ok:blockers.append('Factuur valt buiten actief ALV-uitvoeringsmandaat of budget-lock.')
 if not ref_ok:blockers.append('Contractreferentie op factuur komt niet overeen met geregistreerd contract.')
 if not contract_limit_ok:blockers.append('Factuurbedrag overschrijdt contractwaarde plus tolerantie.')
 if not delivery_ok:blockers.append('Geleverde prestatie is niet volledig geaccepteerd of dekt factuurbedrag niet.')
 if not scope_ok:blockers.append('Factuurscope wijkt af van contractscope.')
 if not period_ok:reviews.append('Factuurperiode wijkt af van contractperiode.')
 if change_order and not change_approved:blockers.append('Meerwerk/wijzigingsopdracht is niet formeel goedgekeurd.')
 status='THREE-WAY MATCH GESLAAGD' if not blockers and not reviews else ('REVIEW VEREIST' if not blockers else 'FACTUUR GEBLOKKEERD')
 return {'invoice_validation_contract_three_way_control_version':ENGINE_VERSION,'validation_id':_id(mandate.get('mandate_id',''),expected_ref,invoice.get('invoice_number',''),amount),'status':status,'invoice_number':invoice.get('invoice_number'),'invoice_amount_eur':round(amount,2),'contract_amount_eur':round(contract_amount,2),'accepted_delivery_value_eur':round(delivered_value,2),'mandate_match':mandate_ok,'contract_reference_match':ref_ok,'contract_amount_match':contract_limit_ok,'delivery_match':delivery_ok,'scope_match':scope_ok,'period_match':period_ok,'change_order_detected':change_order,'change_order_approved':change_approved,'blockers':blockers,'review_items':reviews,'approved_for_payment_workflow':not blockers and not reviews,'human_invoice_approval_required':True,'human_budget_owner_confirmation_required':True,'automatic_payment':False,'automatic_booking':False,'automatic_commitment':False,'next_action':'Laat budgethouder de match bevestigen en stuur daarna door naar betaalworkflow.' if not blockers and not reviews else ('Beoordeel reviewpunten expliciet vóór betaling.' if not blockers else 'Los blockers op; factuur mag niet naar betaling.')}
