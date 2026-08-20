from src.adaptive_vve_financial_digital_twin import build_adaptive_financial_twin

def test_horizons_present():
 x=build_adaptive_financial_twin({}, {'annual_plan':[]}, {'reserve_balance_eur':100000,'cash_balance_eur':20000,'annual_contributions_eur':30000,'annual_operating_cost_eur':10000}); assert [s['horizon_years'] for s in x['snapshots']]==[1,5,10,30]
def test_risk_reduces_health():
 base=build_adaptive_financial_twin({}, {'annual_plan':[]}, {'reserve_balance_eur':10000,'cash_balance_eur':1000,'annual_contributions_eur':1000,'annual_operating_cost_eur':1000}); risky=build_adaptive_financial_twin({}, {'annual_plan':[]}, {'reserve_balance_eur':10000,'cash_balance_eur':1000,'annual_contributions_eur':1000,'annual_operating_cost_eur':1000},{'expected_annual_risk_cost_eur':5000},{'governance_risk_score':50}); assert risky['snapshots'][-1]['financial_health_score']<=base['snapshots'][-1]['financial_health_score']
def test_no_automatic_changes():
 x=build_adaptive_financial_twin({}, {'annual_plan':[]}, {}); assert x['automatic_contribution_change'] is False and x['automatic_mjop_change'] is False
