from datetime import date
from src.mandate_forecast import forecast_mandates

def test_forecast_flags_projected_budget_overrun():
    mandates={"mandates":[{"mandate_id":"MAN-1","budget":100000,"spent_amount":60000,"progress_percent":50,"status":"IN UITVOERING","deadline":"2026-12-31","owner":"Bestuur"}]}
    result=forecast_mandates(mandates,today=date(2026,8,18))
    assert result["high_risk"]==1
    assert result["forecasts"][0]["projected_final_cost"]==120000

def test_forecast_flags_near_deadline_low_progress():
    mandates={"mandates":[{"mandate_id":"MAN-2","budget":100000,"spent_amount":10000,"progress_percent":20,"status":"IN UITVOERING","deadline":"2026-09-01","owner":"Bestuur"}]}
    result=forecast_mandates(mandates,today=date(2026,8,18),warning_days=30)
    assert result["forecasts"][0]["risk"]=="HOOG"
    assert result["status"]=="VROEGE WAARSCHUWING"
