from src.constitutional_activation_cutover_control import prepare_constitutional_cutover
I={'activation_ready':True,'migration_id':'M1','affected_item_count':3,'financial_exposure_eur':5000}
V={'new_version':'2.0','previous_version':'1.0','current_version':{'version':'2.0'}}
def test_ready_cutover():
 a={'approval_status':'AANGENOMEN','decision_authority':'ALV','resolution_reference':'ALV-2026-13','cutover_date':'2026-09-15','post_activation_review_date':'2026-12-15','rollback_version':'1.0','activation_evidence':['migraties compleet']}; x=prepare_constitutional_cutover(I,V,a); assert x['activation_ready'] is True and x['rollback_ready'] is True
def test_blocked_when_migrations_open():
 x=prepare_constitutional_cutover({'activation_ready':False},V,{}); assert 'GEBLOKKEERD' in x['status']
def test_no_automatic_activation():
 x=prepare_constitutional_cutover(I,V,{}); assert x['automatic_activation'] is False and x['automatic_rollback'] is False
