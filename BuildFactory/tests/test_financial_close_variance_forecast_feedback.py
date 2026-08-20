from src.financial_close_variance_forecast_feedback import build_forecast_feedback

def test_material_variance_requires_reforecast():
 c={'close_id':'C1','spent_ledger_eur':110,'accrual_eur':0,'accounts_payable_eur':0}; b={'period_budget_eur':100,'cash_balance_eur':500,'reserve_balance_eur':1000,'mjop_remaining_eur':5000}; x=build_forecast_feedback(c,b); assert x['material_variance'] is True and x['status']=='FORECAST HERIJKING VEREIST'
def test_accrual_updates_cash_forecast():
 c={'spent_ledger_eur':100,'accrual_eur':50,'accounts_payable_eur':20}; b={'period_budget_eur':100,'cash_balance_eur':500}; x=build_forecast_feedback(c,b); assert x['forecast_feedback']['projected_cash_balance_eur']==430
def test_no_automatic_writeback():
 x=build_forecast_feedback({},{}); assert x['automatic_forecast_writeback'] is False and x['automatic_contribution_change'] is False
