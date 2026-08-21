from src.model_drift_root_cause_recalibration import diagnose_model_drift

def test_market_and_risk_causes_are_detected():
 x=diagnose_model_drift({'drift_detected':True},{'market_price_index_change_pct':8,'risk_distribution_shift_pct':6}); assert 'MARKET_PRICE' in [c['code'] for c in x['ranked_root_causes']] and x['requires_monte_carlo_recalibration'] is True
def test_data_quality_requires_gate():
 x=diagnose_model_drift({}, {'data_missing_pct':5}); assert x['requires_data_quality_gate'] is True
def test_no_automatic_recalibration():
 x=diagnose_model_drift({},{}); assert x['automatic_recalibration'] is False and x['automatic_model_update'] is False
