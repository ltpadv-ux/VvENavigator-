from src.scenario_strategy_lock import build_strategy_lock

RADAR={'preferred_scenario':'Duurzaam','scenarios':[{'scenario':'Duurzaam','robustness_score':88,'adjusted_12m_risk':10,'adjusted_mandate_budget':108000,'reserve_pressure_percent':48,'schedule_factor':1.05,'assumptions':{'risk_factor':.85}}]}

def test_requires_human_approval():
    x=build_strategy_lock(RADAR)
    assert x['status']=='BESLUIT VEREIST'
    assert not x['strategy_lock']

def test_approved_strategy_is_locked():
    x=build_strategy_lock(RADAR,{'selected_scenario':'Duurzaam','decision':'GOEDGEKEURD','approved_by':'ALV','rationale':'Beste robuustheid'})
    assert x['status']=='STRATEGIE VERGRENDELD'
    assert x['strategy_lock']['decision_id'].startswith('STR-')

def test_future_deviation_is_detected():
    first=build_strategy_lock(RADAR,{'selected_scenario':'Duurzaam','decision':'GOEDGEKEURD','approved_by':'ALV'})
    changed={'preferred_scenario':'Duurzaam','scenarios':[{'scenario':'Duurzaam','robustness_score':60,'adjusted_12m_risk':45,'adjusted_mandate_budget':130000,'reserve_pressure_percent':70,'schedule_factor':1.05,'assumptions':{}}]}
    second=build_strategy_lock(changed,first)
    assert second['deviation']['status'] in {'AANDACHT','AFWIJKING'}
    assert second['deviation']['score']>0
