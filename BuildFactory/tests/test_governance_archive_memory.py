from src.governance_archive_memory import build_governance_archive_memory

def register():
 return {'resolution':{'resolution_id':'ALVRES-1','meeting_date':'2026-08-01','decision_authority':'ALV','resolution_text':'Voer maatregel A uit','minutes_reference':'NOT-1'},'execution_mandate':{'mandate_id':'ALVMND-1','budget':10000}}
def closure():
 return {'status':'SLUITING & DECHARGE GEREED','resolution_closure_governance_discharge_version':'11.4.0','closure':{'closure_id':'ALVCLS-1','planned_budget':10000,'actual_spend':9500,'delivery_note':'Opgeleverd','final_result':'Doel bereikt','evidence':['factuur','oplevering']},'discharge':{'discharge_id':'ALVDCH-1','minutes_reference':'NOT-2'}}

def test_closed_case_archives_memory():
 x=build_governance_archive_memory(register(),closure(),context={'lessons_learned':['Vroeg aanbesteden werkt']}); assert x['status']=='INSTITUTIONEEL GEHEUGEN BIJGEWERKT'; assert x['latest_memory']['financial_result']['variance']==-500

def test_open_case_not_archived():
 c=closure(); c['status']='SLUITING NOG NIET GEREED'; x=build_governance_archive_memory(register(),c); assert x['status']=='DOSSIER NOG NIET ARCHIVEERBAAR'; assert x['entry_count']==0

def test_existing_memory_is_idempotently_updated():
 first=build_governance_archive_memory(register(),closure(),context={'what_worked':['Heldere scope']}); second=build_governance_archive_memory(register(),closure(),context={'what_worked':['Heldere scope']},archive=first); assert second['entry_count']==1; assert second['latest_memory']['what_worked']==['Heldere scope']
