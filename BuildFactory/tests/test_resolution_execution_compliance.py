from datetime import date
from src.resolution_execution_compliance import evaluate_resolution_execution_compliance

def register():
    return {'status':'BESLUIT AANGENOMEN - MANDAAT GEREED','resolution':{'resolution_id':'ALVRES-1','resolution_text':'Voer dakonderhoud uit conform offerte 2026.'},'execution_mandate':{'mandate_id':'ALVMND-1','owner':'Bestuur','budget':10000,'deadline':'2026-12-31','evidence_required':True,'progress_pct':0,'actual_spend':0,'evidence':[]}}

def test_compliant_execution():
    a={'mandate_id':'ALVMND-1','owner':'Bestuur','actual_spend':9000,'progress_pct':100,'completed':True,'evidence':['factuur'],'within_resolution_scope':True}
    x=evaluate_resolution_execution_compliance(register(),a,date(2026,8,19)); assert x['status']=='CONFORM UITGEVOERD'; assert x['compliance_score']==100.0

def test_budget_overrun_is_critical():
    a={'mandate_id':'ALVMND-1','owner':'Bestuur','actual_spend':12000,'progress_pct':100,'completed':True,'evidence':['factuur'],'within_resolution_scope':True}
    x=evaluate_resolution_execution_compliance(register(),a,date(2026,8,19)); assert x['status']=='KRITIEKE AFWIJKING'; assert any(i['type']=='BUDGET' for i in x['alerts'])

def test_expired_deadline_without_completion_alerts():
    a={'mandate_id':'ALVMND-1','owner':'Bestuur','actual_spend':5000,'progress_pct':50,'evidence':['werkbon'],'within_resolution_scope':True}
    x=evaluate_resolution_execution_compliance(register(),a,date(2027,1,5)); assert x['status']=='AFWIJKING GEVONDEN'; assert any(i['type']=='DEADLINE' for i in x['alerts'])
