from src.intervention_impact_simulator import simulate_intervention_impacts

def test_no_interventions_returns_empty_simulation():
    x=simulate_intervention_impacts({'proposals':[]},{})
    assert x['simulation_count']==0
    assert x['human_decision_required'] is False

def test_financial_intervention_calculates_horizons():
    interventions={'proposals':[{'domain':'FINANCIEEL','kpi':'Reservedruk','estimated_financial_exposure':12000,'decision_authority':'Bestuur/ALV','options':['Herijk bijdrage/reserve-opbouw']}]}
    report={'governance_control_tower':{'kpis':{'reserve':100000,'monthly_per_apartment':200}},'release':{'dataset':{'apartments':34}}}
    x=simulate_intervention_impacts(interventions,report,discount_rate=.03)
    option=x['simulations'][0]['options'][0]
    assert option['monthly_delta']>0
    assert set(option['horizons'])=={'10','20','30'}
    assert option['horizons']['30']['lcc']>option['horizons']['10']['lcc']
