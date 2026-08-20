from src.model_champion_challenger_validation import compare_models

def test_better_challenger_is_promotable():
 c={'model_id':'C','mape_pct':14,'bias_pct':6,'confidence_calibration_pct':88,'model_reliability_score':78,'stress_resilience_score':72}; q={'model_id':'Q','mape_pct':8,'bias_pct':2,'confidence_calibration_pct':94,'model_reliability_score':86,'stress_resilience_score':80}; x=compare_models(c,q); assert x['promotion_recommended'] is True

def test_weak_challenger_is_blocked():
 c={'mape_pct':10,'bias_pct':2,'confidence_calibration_pct':92,'model_reliability_score':85,'stress_resilience_score':80}; q={'mape_pct':25,'bias_pct':12,'confidence_calibration_pct':80,'model_reliability_score':86,'stress_resilience_score':60}; x=compare_models(c,q); assert x['promotion_recommended'] is False and x['blockers']

def test_no_automatic_promotion():
 x=compare_models({},{}); assert x['automatic_model_promotion'] is False and x['automatic_champion_replacement'] is False
