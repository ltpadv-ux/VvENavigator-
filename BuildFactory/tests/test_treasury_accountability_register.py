from src.treasury_accountability_register import build_treasury_accountability_register

def test_only_approved_items_become_actions():
    pack={'agenda_items':[{'agenda_id':'A1','title':'Actie 1','decision':'GOEDGEKEURD'},{'agenda_id':'A2','title':'Actie 2','decision':'NOG TE BESLUITEN'}]}
    x=build_treasury_accountability_register(pack); assert x['action_count']==1

def test_completed_action_requires_evidence():
    pack={'agenda_items':[{'agenda_id':'A1','title':'Actie 1','decision':'GOEDGEKEURD'}]}
    first=build_treasury_accountability_register(pack)
    aid=first['actions'][0]['action_id']
    x=build_treasury_accountability_register(pack,{'actions':[{'action_id':aid,'progress_percent':100,'evidence':['bankafschrift.pdf']} ]})
    assert x['actions'][0]['status']=='AFGEROND'

def test_over_budget_escalates():
    pack={'agenda_items':[{'agenda_id':'A1','title':'Actie 1','decision':'GOEDGEKEURD'}]}
    first=build_treasury_accountability_register(pack); aid=first['actions'][0]['action_id']
    x=build_treasury_accountability_register(pack,{'actions':[{'action_id':aid,'budget':1000,'spent':1200}]})
    assert x['status']=='ESCALATIE VEREIST'; assert x['over_budget_count']==1
