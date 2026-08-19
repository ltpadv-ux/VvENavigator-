from src.treasury_early_warning_calendar import build_treasury_early_warning_calendar

def test_green_calendar_when_no_risks():
    x=build_treasury_early_warning_calendar({'portfolio_treasury_control_tower':{'treasury_score':95}}, {'months':3})
    assert x['status']=='GROEN'
    assert x['action_count']==0

def test_negative_cash_creates_red_action():
    treasury={'vves':[{'vve':'A','timeline':[{'month':'2026-08','closing_cash':-100,'minimum_buffer':500,'negative_cash':True,'below_buffer':True,'mjop_outflow':0}]}]}
    x=build_treasury_early_warning_calendar({'treasury_forecast':treasury},{'months':1})
    assert x['status']=='ROOD'
    assert x['red_action_count']>=1

def test_dscr_warning_creates_action():
    report={'portfolio_liquidity_debt_control':{'vves':[{'vve':'A','dscr':1.3,'refinancing_months':None}]}}
    x=build_treasury_early_warning_calendar(report,{'months':1})
    assert x['status']=='ORANJE'
    assert any(a['category']=='DSCR' for a in x['actions'])
