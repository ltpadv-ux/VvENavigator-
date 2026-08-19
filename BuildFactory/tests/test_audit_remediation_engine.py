from src.audit_remediation_engine import build_audit_remediation

def test_no_failed_controls():
 x=build_audit_remediation({'treasury_audit_assurance':{'results':[]}}); assert x['status']=='GEEN HERSTELACTIES'

def test_failed_control_creates_owned_action():
 report={'treasury_audit_assurance':{'results':[{'lineage_id':'TRLIN-1','agenda_id':'A1','assurance_score':60,'failed_controls':['BUDGETCONTROLE']}]}}
 x=build_audit_remediation(report); assert x['open_count']==1; assert x['actions'][0]['owner']=='Penningmeester'; assert x['actions'][0]['priority']=='HOOG'

def test_successful_retest_proves_remediation():
 report={'treasury_audit_assurance':{'results':[{'lineage_id':'TRLIN-1','agenda_id':'A1','assurance_score':70,'failed_controls':['EFFECTMETING']}]}}
 first=build_audit_remediation(report); rid=first['actions'][0]['remediation_id']; existing={'actions':[{'remediation_id':rid,'retest':{'passed':True,'tested_by':'Control','evidence':['bewijs']}}]}
 x=build_audit_remediation(report,existing); assert x['status']=='CONTROLS HERSTELD'; assert x['proven_count']==1
