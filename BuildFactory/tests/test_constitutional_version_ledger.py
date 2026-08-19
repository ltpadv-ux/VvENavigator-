from src.constitutional_version_ledger import apply_approved_amendment

def approved():
 return {'ready_for_controlled_processing':True,'amendment':{'amendment_id':'A1','target':'GOVERNANCE_CONSTITUTION','version_from':'1.0','version_to':'2.0','effective_date':'2026-09-01','review_date':'2027-09-01','resolution_reference':'ALV-1','rationale':'Herijking'}}
def test_preserves_previous_version():
 x=apply_approved_amendment(approved(),{'constitution_id':'C1','version':'1.0'}); assert x['status']=='AMENDMENT GECONTROLEERD VERWERKT'; assert x['ledger']['versions'][0]['immutable'] is True; assert x['new_version']=='2.0'
def test_rejects_unapproved():
 x=apply_approved_amendment({'ready_for_controlled_processing':False},{'version':'1.0'}); assert x['status']=='AMENDMENT NIET TOEPASBAAR'
def test_requires_target_version():
 a=approved(); a['amendment']['version_to']=''; x=apply_approved_amendment(a,{'version':'1.0'}); assert x['status']=='DOELVERSIE ONTBREEKT'
