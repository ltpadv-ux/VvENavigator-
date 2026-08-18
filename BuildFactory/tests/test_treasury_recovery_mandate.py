from src.treasury_recovery_mandate import build_treasury_recovery_mandate

STRESS={'status':'CRITIEK','preferred_intervention':{'action':'MJOP FASEREN','decision_authority':'Bestuur/ALV'}}
TREASURY={'negative_cash_count':1,'buffer_breach_count':2,'portfolio_timeline':[{'month':'2027-01','minimum_buffer':10000,'below_buffer':True,'negative_cash':False},{'month':'2027-02','minimum_buffer':10000,'below_buffer':True,'negative_cash':True}]}

def test_requires_human_decision():
    x=build_treasury_recovery_mandate(STRESS,TREASURY)
    assert x['status']=='BESLUIT VEREIST'
    assert x['automatic_execution'] is False

def test_approved_decision_creates_mandate():
    existing={'decision':{'selected_action':'MJOP FASEREN','decision':'GOEDGEKEURD','approved_by':'ALV'}}
    x=build_treasury_recovery_mandate(STRESS,TREASURY,existing)
    assert x['status']=='HERSTELMANDAAT ACTIEF'
    assert x['mandate']['mandate_id'].startswith('TRMAN-')
    assert x['mandate']['target_negative_cash_months']==0

def test_recovery_requires_effect_proof():
    existing={'decision':{'selected_action':'MJOP FASEREN','decision':'GOEDGEKEURD','approved_by':'ALV'},'tracking':{'progress_percent':100,'actual_minimum_cash':12000,'negative_cash_months':0,'buffer_breach_months':0}}
    x=build_treasury_recovery_mandate(STRESS,TREASURY,existing)
    assert x['status']=='HERSTEL BEWEZEN'
    assert x['tracking']['recovery_proven'] is True
