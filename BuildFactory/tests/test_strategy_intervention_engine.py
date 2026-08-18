from src.strategy_intervention_engine import build_strategy_interventions

def test_no_intervention_when_on_track():
    x=build_strategy_interventions({'status':'OP KOERS','kpis':[{'domain':'FINANCIEEL','on_track':True}]},{}); assert x['status']=='GEEN INTERVENTIE'; assert x['proposal_count']==0

def test_attention_creates_human_proposal():
    score={'status':'AANDACHT','decision_id':'STR-1','selected_scenario':'Duurzaam','kpis':[{'domain':'RISICO','kpi':'12-maands risicodruk','target':10,'actual':25,'on_track':False}]}
    x=build_strategy_interventions(score,{}); assert x['status']=='VOORSTEL VEREIST'; assert x['proposals'][0]['approval_required'] is True; assert x['automatic_strategy_change'] is False

def test_outside_course_escalates():
    score={'status':'BUITEN KOERS','kpis':[{'domain':'FINANCIEEL','kpi':'Reservedruk','target':50,'actual':90,'on_track':False},{'domain':'COMPLIANCE','kpi':'Rode mandaten','target':0,'actual':2,'on_track':False}]}
    report={'governance_control_tower':{'kpis':{'reserve':100000,'total_mandate_budget':130000}}}
    x=build_strategy_interventions(score,report); assert x['status']=='BESTUURLIJKE INTERVENTIE VEREIST'; assert x['proposal_count']==2; assert x['proposals'][0]['estimated_financial_exposure']==30000
