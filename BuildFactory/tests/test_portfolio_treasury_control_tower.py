from src.portfolio_treasury_control_tower import build_portfolio_treasury_control_tower

def test_green_tower_when_no_issues():
    r={'portfolio_intelligence':{'portfolio_count':2},'portfolio_funding_covenant_control':{'breach_count':0,'warning_count':0},'portfolio_liquidity_debt_control':{'breach_count':0,'warning_count':0,'total_debt':100000,'annual_debt_service':12000,'portfolio_dscr':1.8},'treasury_forecast':{'negative_cash_count':0,'buffer_breach_count':0},'treasury_stress_intervention':{'critical_scenario_count':0,'attention_scenario_count':0},'treasury_recovery_mandate':{'status':'GEEN HERSTEL NODIG'},'treasury_recovery_effectiveness':{'status':'NIET VAN TOEPASSING','closure_status':'OPEN','stable_periods':0}}
    x=build_portfolio_treasury_control_tower(r); assert x['status']=='GROEN'; assert x['treasury_score']==100

def test_red_tower_prioritizes_negative_cash():
    r={'portfolio_funding_covenant_control':{'breach_count':1,'warning_count':0},'portfolio_liquidity_debt_control':{'breach_count':1,'warning_count':0},'treasury_forecast':{'negative_cash_count':1,'buffer_breach_count':1},'treasury_stress_intervention':{'critical_scenario_count':1},'treasury_recovery_mandate':{'status':'HERSTELMANDAAT ACTIEF'},'treasury_recovery_effectiveness':{'status':'NADER HERSTEL NODIG','closure_status':'OPEN'}}
    x=build_portfolio_treasury_control_tower(r); assert x['status']=='ROOD'; assert x['priority_actions'][0].startswith('Herstel negatieve kasposities')

def test_human_governance_is_preserved():
    x=build_portfolio_treasury_control_tower({}); assert x['human_governance_preserved'] is True; assert x['automatic_cash_transfer'] is False
