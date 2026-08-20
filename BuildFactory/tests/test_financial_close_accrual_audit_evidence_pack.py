from src.financial_close_accrual_audit_evidence_pack import build_financial_close

def test_audit_ready_close():
 ledger=[{'entry_type':'COMMITMENT','amount_eur':100},{'entry_type':'PAYMENT','amount_eur':80}]; inv=[{'invoice_number':'I1','supplier_id':'S1','amount_eur':80,'paid':True}]; rec=[{'status':'BETALING VOLLEDIG GERECONCILIEERD'}]; x=build_financial_close('2026-08',ledger,inv,rec); assert x['audit_ready'] is True and x['accrual_eur']==20
def test_unreconciled_blocks():
 x=build_financial_close('2026-08',[],[{'invoice_number':'I1','supplier_id':'S1','amount_eur':10}], [{'status':'REVIEW'}]); assert x['audit_ready'] is False
def test_no_automatic_close():
 x=build_financial_close('2026-08',[],[],[]); assert x['automatic_close'] is False and x['automatic_journal_posting'] is False
