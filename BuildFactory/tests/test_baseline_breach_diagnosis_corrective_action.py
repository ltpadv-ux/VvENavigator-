from src.baseline_breach_diagnosis_corrective_action import diagnose_baseline_breach

def test_scope_breach_requires_new_resolution():
 x=diagnose_baseline_breach({'baseline_breach':True},{'scope_variance_eur':10000},{'baseline_id':'B1'}); assert x['requires_new_formal_resolution'] is True and 'SCOPE' in x['cause_codes']
def test_cash_and_reserve_breach_require_board_review():
 x=diagnose_baseline_breach({}, {'cash_eur':80,'reserve_eur':80},{'cash_eur':100,'reserve_eur':100}); assert x['requires_board_review'] is True and x['requires_reforecast'] is True
def test_no_automatic_correction():
 x=diagnose_baseline_breach({}, {}, {}); assert x['automatic_corrective_action'] is False and x['automatic_baseline_change'] is False
