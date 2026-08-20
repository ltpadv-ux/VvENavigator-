from src.payment_reconciliation_bank_statement_control import reconcile_payment
P={'payment_control_id':'P1','status':'BETALING GEREED VOOR HANDMATIGE VRIJGAVE','payment_amount_eur':1000,'supplier_id':'S1','invoice_number':'INV1'}
def test_reconciled_payment():
 b={'transaction_id':'T1','amount_eur':1000,'supplier_id':'S1','invoice_number':'INV1','iban':'NL00BANK123','expected_iban':'NL00BANK123'}; l={'payment_amount_eur':1000}; x=reconcile_payment(P,b,l); assert x['reconciled'] is True
def test_duplicate_blocks():
 b={'amount_eur':1000,'supplier_id':'S1','invoice_number':'INV1','iban':'NL00BANK123','expected_iban':'NL00BANK123'}; l={'amount_eur':1000}; h=[{'invoice_number':'INV1','supplier_id':'S1','amount_eur':1000}]; assert reconcile_payment(P,b,l,h)['reconciled'] is False
def test_reversal_requires_review():
 b={'amount_eur':1000,'supplier_id':'S1','invoice_number':'INV1','iban':'NL00BANK123','expected_iban':'NL00BANK123','reversed':True}; l={'amount_eur':1000}; x=reconcile_payment(P,b,l); assert x['reconciled'] is False and x['automatic_reversal_handling'] is False
