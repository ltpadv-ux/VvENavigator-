from src.treasury_stress_intervention import build_treasury_stress_interventions

BASE={'vves':[{'vve':'A','opening_cash':50000,'timeline':[{'month':'2026-09','closing_cash':45000,'minimum_buffer':10000,'contributions':20000,'other_income':0,'subsidy':0,'interest_income':100,'operating_outflow':10000,'debt_service':2000,'mjop_outflow':13000,'other_outflow':0}]}]}

def test_robust_treasury_stays_robust_under_mild_custom_stress():
    x=build_treasury_stress_interventions(BASE,{'MILD':{'operating_factor':1.01}})
    assert x['status']=='ROBUUST'
    assert x['automatic_execution'] is False

def test_negative_cash_creates_critical_status():
    bad={'vves':[{'vve':'A','opening_cash':1000,'timeline':[{'month':'2026-09','closing_cash':500,'minimum_buffer':1000,'contributions':1000,'other_income':0,'subsidy':0,'interest_income':0,'operating_outflow':1000,'debt_service':0,'mjop_outflow':500,'other_outflow':0}]}]}
    x=build_treasury_stress_interventions(bad,{'SHOCK':{'operating_factor':2.0}})
    assert x['status']=='CRITIEK'
    assert x['human_decision_required'] is True

def test_interventions_are_ranked():
    x=build_treasury_stress_interventions(BASE,{'SHOCK':{'mjop_shift_months':-6}})
    assert x['interventions']
    assert x['interventions'][0]['score'] >= x['interventions'][-1]['score']
