from datetime import date
from src.waiver_monitoring_constitutional_debt import monitor_waivers

def test_no_waivers_green():
 x=monitor_waivers([],date(2026,8,19)); assert x['constitutional_debt_level']=='GROEN'
def test_expired_waiver_increases_debt():
 w={'status':'WAIVER VERLOPEN','waiver':{'waiver_id':'W1','scope':'MJOP','valid_from':'2026-01-01','valid_until':'2026-06-01','financial_impact_eur':1000}}; x=monitor_waivers([w],date(2026,8,19)); assert x['expired_waivers']==1; assert x['constitutional_debt_score']>0
def test_repeated_scope_detected():
 ws=[{'status':'WAIVER ACTIEF','waiver':{'waiver_id':'W1','scope':'Finance','valid_from':'2026-08-01'}},{'status':'WAIVER ACTIEF','waiver':{'waiver_id':'W2','scope':'Finance','valid_from':'2026-08-05'}}]; x=monitor_waivers(ws,date(2026,8,19)); assert x['repeated_exception_patterns'][0]['scope']=='Finance'
