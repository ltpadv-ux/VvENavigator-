from src.controlled_model_promotion_version_freeze_rollback import promote_model,evaluate_rollback

def test_clean_promotion_freezes_old_champion():
 x=promote_model({'model_id':'C1','version':'1.0'},{'model_id':'Q1','version':'2.0'},{'promotion_review_ready':True,'shadow_run_id':'S1'},{'model_owner_approved':True,'board_approved':True,'final_monte_carlo_passed':True,'promotion_date':'2026-08-21'}); assert x['promotion_authorized'] is True and x['former_champion_archive']['immutable'] is True
def test_missing_board_approval_blocks():
 x=promote_model({'model_id':'C1'},{'model_id':'Q1'},{'promotion_review_ready':True},{'model_owner_approved':True,'final_monte_carlo_passed':True,'promotion_date':'2026-08-21'}); assert x['promotion_authorized'] is False
def test_rollback_is_review_only():
 p=promote_model({'model_id':'C1'},{'model_id':'Q1'},{'promotion_review_ready':True},{'model_owner_approved':True,'board_approved':True,'final_monte_carlo_passed':True,'promotion_date':'2026-08-21'}); r=evaluate_rollback(p,{'reliability_drop_points':6,'live_mape_pct':10}); assert r['rollback_recommended'] is True and r['automatic_rollback'] is False
