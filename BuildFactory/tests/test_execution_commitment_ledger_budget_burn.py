from src.execution_commitment_ledger_budget_burn import build_commitment_ledger, assess_new_ledger_entry
M={'mandate_id':'M1','maximum_commitment_eur':100000,'budget_lock_active':True}
def test_ledger_within_mandate():
 x=build_commitment_ledger(M,[{'type':'RESERVATION','amount_eur':20000},{'type':'CONTRACT','amount_eur':50000},{'type':'INVOICE','amount_eur':30000}]); assert x['status']=='BUDGET BURN BINNEN MANDAAT' and x['available_after_commitments_eur']==50000
def test_over_budget_blocks():
 x=build_commitment_ledger(M,[{'type':'CONTRACT','amount_eur':120000}]); assert 'BLOKKADE' in x['status']
def test_new_entry_guard():
 l=build_commitment_ledger(M,[{'type':'CONTRACT','amount_eur':90000}]); y=assess_new_ledger_entry(l,{'type':'CONTRACT','amount_eur':15000}); assert y['allowed'] is False and y['automatic_posting'] is False
