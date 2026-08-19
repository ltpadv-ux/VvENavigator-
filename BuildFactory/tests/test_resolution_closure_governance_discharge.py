from src.resolution_closure_governance_discharge import close_resolution_and_discharge

def register():
 return {'status':'BESLUIT AANGENOMEN - MANDAAT GEREED','resolution':{'resolution_id':'ALVRES-1','minutes_reference':'NOT-1'},'execution_mandate':{'mandate_id':'ALVMND-1','budget':10000,'progress_pct':100,'actual_spend':9000,'evidence':['bewijs']}}

def compliant():
 return {'status':'CONFORM UITGEVOERD','alerts':[],'actual_spend':9000}

def test_ready_for_discharge():
 x=close_resolution_and_discharge(register(),compliant(),{'completed':True,'progress_pct':100,'actual_spend':9000,'delivery_note':'opgeleverd','final_result':'doel bereikt','evidence':['bewijs'],'governance_review':'GOEDGEKEURD'})
 assert x['status']=='SLUITING & DECHARGE GEREED'; assert x['discharge']['discharge_id'].startswith('ALVDCH-')

def test_noncompliant_execution_blocks_closure():
 c={'status':'KRITIEKE AFWIJKING','alerts':[{'severity':'ROOD'}]}
 x=close_resolution_and_discharge(register(),c,{'completed':True,'delivery_note':'opgeleverd','final_result':'gereed','evidence':['bewijs'],'governance_review':'GOEDGEKEURD'})
 assert x['status']=='KRITIEKE AFWIJKING - NIET SLUITEN'; assert x['discharge']=={}

def test_missing_governance_review_blocks_discharge():
 x=close_resolution_and_discharge(register(),compliant(),{'completed':True,'progress_pct':100,'actual_spend':9000,'delivery_note':'opgeleverd','final_result':'doel bereikt','evidence':['bewijs']})
 assert x['status']=='SLUITING NOG NIET GEREED'; assert x['closure']['checks']['governance_review_approved'] is False
