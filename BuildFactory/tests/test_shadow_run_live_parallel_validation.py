from src.shadow_run_live_parallel_validation import validate_shadow_run

def test_shadow_run_can_pass():
 c=[{'period':'P1','mape_pct':12,'bias_pct':5,'reliability_score':80},{'period':'P2','mape_pct':11,'bias_pct':4,'reliability_score':81},{'period':'P3','mape_pct':13,'bias_pct':6,'reliability_score':79}]
 q=[{'period':'P1','mape_pct':8,'bias_pct':3,'reliability_score':84},{'period':'P2','mape_pct':9,'bias_pct':3,'reliability_score':85},{'period':'P3','mape_pct':10,'bias_pct':4,'reliability_score':83}]
 x=validate_shadow_run(c,q); assert x['promotion_review_ready'] is True and x['challenger_win_rate_pct']==100

def test_too_few_periods_blocks():
 x=validate_shadow_run([{'mape_pct':10,'reliability_score':80}],[{'mape_pct':8,'reliability_score':84}]); assert x['promotion_review_ready'] is False

def test_no_automatic_promotion():
 x=validate_shadow_run([],[]); assert x['automatic_model_promotion'] is False and x['automatic_champion_replacement'] is False
