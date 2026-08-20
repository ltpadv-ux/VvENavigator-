from src.model_backtesting_forecast_accuracy_scorecard import build_backtest_scorecard

def test_good_backtest_is_reliable():
 r=[{'year':2024,'component':'DAK','forecast_eur':100,'actual_eur':105,'p05_eur':90,'p95_eur':120},{'year':2025,'component':'DAK','forecast_eur':100,'actual_eur':102,'p05_eur':90,'p95_eur':120},{'year':2026,'component':'DAK','forecast_eur':100,'actual_eur':98,'p05_eur':90,'p95_eur':120}]; x=build_backtest_scorecard(r); assert x['status']=='BETROUWBAAR MODEL' and x['model_reliability_score']>=80

def test_bad_backtest_requires_recalibration():
 r=[{'forecast_eur':100,'actual_eur':200},{'forecast_eur':100,'actual_eur':200},{'forecast_eur':100,'actual_eur':200}]; x=build_backtest_scorecard(r); assert x['requires_recalibration'] is True

def test_no_automatic_model_update():
 x=build_backtest_scorecard([]); assert x['automatic_model_update'] is False and x['automatic_baseline_change'] is False
