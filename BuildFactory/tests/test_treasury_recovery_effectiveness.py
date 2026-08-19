from src.treasury_recovery_effectiveness import evaluate_treasury_recovery_effectiveness

def test_not_applicable_before_recovery_decision():
    x=evaluate_treasury_recovery_effectiveness({'status':'BESLUIT VEREIST'},{},{},{})
    assert x['status']=='NIET VAN TOEPASSING'

def test_stability_builds_before_closure():
    recovery={'status':'EFFECTCONTROLE','tracking':{'progress_percent':100}}
    treasury={'negative_cash_count':0,'buffer_breach_count':0,'portfolio_timeline':[{'negative_cash':False,'below_buffer':False} for _ in range(3)]}
    liquidity={'vves':[{'dscr':1.5}]}; funding={'breach_count':0}; forecast={'high_risk_count':0}
    x=evaluate_treasury_recovery_effectiveness(recovery,treasury,liquidity,funding,forecast)
    assert x['status']=='STABILITEIT OPBOUWEN'; assert x['stable_periods']==1

def test_closes_after_required_stable_runs():
    recovery={'status':'EFFECTCONTROLE','tracking':{'progress_percent':100}}
    treasury={'negative_cash_count':0,'buffer_breach_count':0,'portfolio_timeline':[{'negative_cash':False,'below_buffer':False} for _ in range(3)]}
    liquidity={'vves':[{'dscr':1.6}]}; funding={'breach_count':0}; forecast={'high_risk_count':0}
    state={'stable_periods':2}
    x=evaluate_treasury_recovery_effectiveness(recovery,treasury,liquidity,funding,forecast,state)
    assert x['status']=='HERSTEL DUURZAAM BEWEZEN'; assert x['closure_status']=='GESLOTEN'; assert x['automatic_closure'] is False
