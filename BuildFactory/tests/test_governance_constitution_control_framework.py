from src.governance_constitution_control_framework import build_governance_constitution

def test_requires_approved_doctrine():
 x=build_governance_constitution({'baseline_id':'B1','doctrines':[{'status':'CONCEPT DOCTRINE','topic':'MJOP'}]}); assert x['status']=='CONSTITUTIONEEL RAAMWERK ONVOLLEDIG'

def test_approved_doctrine_makes_framework_ready():
 d={'baseline_id':'B1','doctrines':[{'doctrine_id':'D1','status':'VASTGESTELD','topic':'MJOP','strategic_principle':'Risicogestuurd onderhouden','consistency_confidence':90}]}; x=build_governance_constitution(d); assert x['status']=='CONSTITUTIONEEL RAAMWERK GEREED VOOR VASTSTELLING'; assert x['constitution_id'].startswith('GOVCONST-')

def test_no_automatic_governance_actions():
 d={'doctrines':[{'approved':True,'topic':'Finance','strategic_principle':'Behoud reservebuffer'}]}; x=build_governance_constitution(d); assert x['automatic_decision'] is False and x['automatic_execution'] is False
