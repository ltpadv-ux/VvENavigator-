from src.treasury_forecast import build_treasury_forecast

def test_healthy_cash_plan():
    liquidity={'vves':[{'vve':'A','liquid_reserve':120000,'annual_debt_service':12000}]}
    actuals={'A':{'monthly_contributions':15000,'monthly_operating_outflow':10000}}
    x=build_treasury_forecast(liquidity,actuals,{'months':12,'minimum_cash_buffer_months':3})
    assert x['status']=='VOLDOENDE LIQUIDITEIT'
    assert len(x['vves'][0]['timeline'])==12

def test_buffer_breach_detected():
    liquidity={'vves':[{'vve':'A','liquid_reserve':25000,'annual_debt_service':12000}]}
    actuals={'A':{'monthly_contributions':10000,'monthly_operating_outflow':9000}}
    x=build_treasury_forecast(liquidity,actuals,{'months':6,'minimum_cash_buffer_months':3})
    assert x['status'] in {'BUFFER BREACH','NEGATIEVE KAS'}

def test_mjop_outflow_can_create_negative_cash():
    liquidity={'vves':[{'vve':'A','liquid_reserve':10000,'annual_debt_service':0}]}
    actuals={'A':{'monthly_contributions':1000,'monthly_operating_outflow':1000}}
    first=build_treasury_forecast(liquidity,actuals,{'months':2,'minimum_cash_buffer_months':0})
    month=first['vves'][0]['timeline'][0]['month']; actuals['A']['mjop_outflows']={month:20000}
    second=build_treasury_forecast(liquidity,actuals,{'months':2,'minimum_cash_buffer_months':0})
    assert second['status']=='NEGATIEVE KAS'
