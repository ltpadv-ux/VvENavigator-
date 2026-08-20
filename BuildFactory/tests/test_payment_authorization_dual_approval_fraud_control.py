from src.payment_authorization_dual_approval_fraud_control import authorize_payment

def test_ready_for_manual_release():
 t={'status':'THREE-WAY MATCH GESLAAGD'}; p={'invoice_number':'INV-1','supplier_id':'S1','iban':'NL01BANK123','amount_eur':1000,'approvers':['A','B']}; v={'supplier_id':'S1','verified_iban':'NL01BANK123'}; x=authorize_payment(t,p,v); assert x['ready_for_manual_release'] is True

def test_duplicate_blocks():
 t={'status':'THREE-WAY MATCH GESLAAGD'}; p={'invoice_number':'INV-1','supplier_id':'S1','iban':'NL01BANK123','amount_eur':1000,'approvers':['A','B']}; v={'supplier_id':'S1','verified_iban':'NL01BANK123'}; h=[{'invoice_number':'INV-1','supplier_id':'S1'}]; assert authorize_payment(t,p,v,h)['status']=='BETALING GEBLOKKEERD'

def test_dual_approval_required():
 t={'status':'THREE-WAY MATCH GESLAAGD'}; p={'invoice_number':'INV-2','supplier_id':'S1','iban':'NL01BANK123','amount_eur':1000,'approvers':['A']}; v={'supplier_id':'S1','verified_iban':'NL01BANK123'}; x=authorize_payment(t,p,v); assert x['dual_approval_ok'] is False and x['automatic_payment'] is False
