from src.strategic_amendment_effectiveness import evaluate_amendment_effectiveness

def amendment():
 return {'status':'MANDAATWIJZIGING GOEDGEKEURD','amendment':{'amendment_id':'PSMA-1'},'amended_mandate':{'mandate_id':'PSM-1','kpi_targets':[{'month':12,'target_score':85}]}}
def green(): return {'status':'GROEN','variances':{'governance_score_variance':0,'contribution_delta_variance':0,'mjop_acceleration_variance':0,'budget_variance':0}}
def actuals(): return {'governance_score':86,'audit_assurance_score':90,'treasury_status':'GROEN','finance':{'score':85},'mjop':{'score':85},'treasury':{'score':90},'governance':{'score':86},'evidence':['meting']}

def test_first_green_period_not_rebaseline_yet():
 x=evaluate_amendment_effectiveness(amendment(),green(),actuals()); assert x['status']=='EFFECTMETING ACTIEF'; assert x['stable_periods']==1

def test_second_green_period_creates_rebaseline():
 first=evaluate_amendment_effectiveness(amendment(),green(),actuals()); x=evaluate_amendment_effectiveness(amendment(),green(),actuals(),first); assert x['status']=='WIJZIGING EFFECTIEF - RE-BASELINE GEREED'; assert x['rebaseline']['baseline_id'].startswith('PSRB-')

def test_red_variance_resets_stability():
 v=green(); v['status']='ROOD'; x=evaluate_amendment_effectiveness(amendment(),v,actuals(),{'stable_periods':1}); assert x['stable_periods']==0; assert x['status']=='NADER HERSTEL NODIG'
