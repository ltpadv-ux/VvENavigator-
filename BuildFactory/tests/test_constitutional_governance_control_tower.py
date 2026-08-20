from src.constitutional_governance_control_tower import build_control_tower

def test_on_course():
 x=build_control_tower(version={'current_version':{'version':'2.0'}},gate={'gate':'GO','compliance_score':100},debt={'constitutional_debt_score':0,'constitutional_debt_level':'GROEN','active_waivers':0},migration={'open_migration_count':0},assurance={'assurance_score':95,'decision':'BEHOUDEN'}); assert x['status']=='OP KOERS'
def test_critical_rollback():
 x=build_control_tower(gate={'gate':'GO','compliance_score':90},debt={'constitutional_debt_score':20,'constitutional_debt_level':'GEEL'},assurance={'assurance_score':50,'decision':'ROLLBACK'}); assert x['status']=='DIRECT BESTUURLIJK BESLUIT VEREIST'
def test_no_automatic_actions():
 x=build_control_tower(); assert x['automatic_decision'] is False and x['automatic_rollback'] is False
