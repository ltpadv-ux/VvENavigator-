from src.treasury_decision_effectiveness import evaluate_treasury_decision_effectiveness

def base_report():
    return {'treasury_forecast':{'negative_cash_count':0,'buffer_breach_count':0},'portfolio_liquidity_debt_control':{'vves':[{'dscr':1.5}]},'portfolio_funding_covenant_control':{'breach_count':0},'mandate_forecast':{'high_risk_count':0},'treasury_stress_intervention':{'critical_scenario_count':0}}

def test_no_actions():
    x=evaluate_treasury_decision_effectiveness({'actions':[]},base_report()); assert x['status']=='GEEN ACTIES'

def test_completed_action_builds_stability():
    accountability={'actions':[{'action_id':'TRACT-1','agenda_id':'A1','title':'Herstel buffer','status':'AFGEROND','evidence':['bewijs.pdf']}]}
    x=evaluate_treasury_decision_effectiveness(accountability,base_report()); assert x['closures'][0]['status']=='STABILITEIT OPBOUWEN'; assert x['closures'][0]['stable_periods']==1

def test_second_stable_period_closes():
    accountability={'actions':[{'action_id':'TRACT-1','agenda_id':'A1','title':'Herstel buffer','status':'AFGEROND','evidence':['bewijs.pdf']}]}
    existing={'closures':[{'action_id':'TRACT-1','stable_periods':1}]}
    x=evaluate_treasury_decision_effectiveness(accountability,base_report(),existing); assert x['closures'][0]['closure_status']=='GESLOTEN'; assert x['status']=='VOLLEDIG EFFECTIEF'

def test_new_covenant_problem_blocks_closure():
    accountability={'actions':[{'action_id':'TRACT-1','agenda_id':'A1','title':'Herstel buffer','status':'AFGEROND','evidence':['bewijs.pdf']}]}
    report=base_report(); report['portfolio_funding_covenant_control']['breach_count']=1
    x=evaluate_treasury_decision_effectiveness(accountability,report,{'closures':[{'action_id':'TRACT-1','stable_periods':1}]}); assert x['closures'][0]['closure_status']=='OPEN'; assert x['closures'][0]['stable_periods']==0
