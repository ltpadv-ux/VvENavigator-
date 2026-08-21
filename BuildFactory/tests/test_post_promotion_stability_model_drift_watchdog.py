from src.post_promotion_stability_model_drift_watchdog import monitor_post_promotion_stability

def test_stable_champion():
 p={'new_champion':{'model_id':'M2'}}; b={'mape_pct':8,'reliability_score':90,'confidence_calibration_pct':92,'combined_shortfall_pct':4}; live=[{'mape_pct':8,'bias_pct':1,'reliability_score':90,'confidence_calibration_pct':92,'combined_shortfall_pct':4}]*3; x=monitor_post_promotion_stability(p,live,b); assert x['status']=='NIEUWE CHAMPION STABIEL'
def test_critical_drift_triggers_rollback_review():
 p={'new_champion':{'model_id':'M2'}}; b={'mape_pct':8,'reliability_score':90,'confidence_calibration_pct':92,'combined_shortfall_pct':4}; live=[{'mape_pct':26,'bias_pct':12,'reliability_score':82,'confidence_calibration_pct':80,'combined_shortfall_pct':9}]*3; x=monitor_post_promotion_stability(p,live,b); assert x['rollback_review_required'] is True
def test_no_automatic_rollback():
 x=monitor_post_promotion_stability({},[],{}); assert x['automatic_rollback'] is False and x['automatic_model_change'] is False
