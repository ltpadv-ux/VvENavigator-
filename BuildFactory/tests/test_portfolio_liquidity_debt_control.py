from src.portfolio_liquidity_debt_control import build_portfolio_liquidity_control

FUNDING={'decisions':[{'decision_id':'FUND-1','vve':'A','approved':True,'funding_mix':{'loan_amount':120000},'covenants':[{'covenant':'RENTE','actual':0.04}]}]}

def test_requires_actuals_for_debt_monitoring():
    x=build_portfolio_liquidity_control(FUNDING)
    assert x['status']=='DATA AANVULLEN'
    assert x['data_required_count']==1

def test_healthy_dscr_and_liquidity():
    actuals={'A':{'annual_cash_inflow':180000,'annual_operating_outflow':120000,'liquid_reserve':90000,'refinancing_months':60}}
    x=build_portfolio_liquidity_control(FUNDING,actuals)
    assert x['status']=='GEZOND'
    assert x['vves'][0]['dscr']>1.25
    assert x['vves'][0]['liquidity_months']>=6

def test_breach_when_cash_cover_and_liquidity_are_low():
    actuals={'A':{'cash_available_for_debt_service':5000,'annual_operating_outflow':120000,'liquid_reserve':10000,'refinancing_months':12}}
    x=build_portfolio_liquidity_control(FUNDING,actuals)
    assert x['status']=='BREACH'
    assert 'DSCR' in x['vves'][0]['breaches']
    assert 'LIQUIDITEITSBUFFER' in x['vves'][0]['breaches']
