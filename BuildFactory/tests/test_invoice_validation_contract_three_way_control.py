from src.invoice_validation_contract_three_way_control import validate_invoice_three_way

M={'mandate_id':'M1','budget_lock_active':True,'maximum_commitment_eur':10000}
C={'contract_reference':'C1','contract_amount_eur':5000,'scope':'Schilderwerk','period':'2026-Q4'}
D={'accepted':True,'accepted_value_eur':5000}
def test_three_way_match_passes():
 i={'invoice_number':'I1','contract_reference':'C1','amount_eur':5000,'scope':'Schilderwerk','period':'2026-Q4'}; x=validate_invoice_three_way(M,C,D,i); assert x['status']=='THREE-WAY MATCH GESLAAGD' and x['approved_for_payment_workflow'] is True
def test_unapproved_change_order_blocks():
 i={'invoice_number':'I2','contract_reference':'C1','amount_eur':5000,'scope':'Schilderwerk','period':'2026-Q4','change_order':True,'change_order_approved':False}; assert validate_invoice_three_way(M,C,D,i)['status']=='FACTUUR GEBLOKKEERD'
def test_no_automatic_payment():
 i={'invoice_number':'I3','contract_reference':'C1','amount_eur':4000,'scope':'Schilderwerk','period':'2026-Q4'}; x=validate_invoice_three_way(M,C,D,i); assert x['automatic_payment'] is False and x['automatic_booking'] is False
