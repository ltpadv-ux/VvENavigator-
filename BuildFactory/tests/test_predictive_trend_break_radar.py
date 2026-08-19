from src.predictive_trend_break_radar import build_predictive_trend_break_radar

def run(v): return {'kpis':{'financial_health':v,'risk_score':100-v}}

def test_insufficient_history():
 x=build_predictive_trend_break_radar({'runs':[run(80),run(80),run(80)]}); assert x['status']=='TREND OPBOUWEN'

def test_finance_reversal_detected():
 hist={'runs':[run(82),run(83),run(84),run(82),run(79)]}; x=build_predictive_trend_break_radar(hist); assert x['domain_signals']['financial_health']['trend_break'] is True; assert x['alert_count']>=1

def test_stable_series_no_alert():
 hist={'runs':[run(80),run(80.2),run(80.1),run(80.2),run(80.1)]}; x=build_predictive_trend_break_radar(hist); assert x['status']=='GEEN TRENDBREUK'; assert x['automatic_intervention'] is False
