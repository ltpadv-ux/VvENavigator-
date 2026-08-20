from src.constitutional_governance_pulse import build_governance_pulse

def test_stable_pulse():
 c={'tower_id':'T2','decision_gate':'GO','active_waivers':0,'constitutional_debt_score':10,'open_migrations':0,'assurance_decision':'BEHOUDEN','constitutional_health_score':90}; p={**c,'tower_id':'T1'}; x=build_governance_pulse(c,p); assert x['status']=='STABIEL' and x['exception_count']==0

def test_new_block_is_critical():
 p={'decision_gate':'GO','assurance_decision':'BEHOUDEN','constitutional_health_score':90}; c={'decision_gate':'BLOCK','assurance_decision':'BEHOUDEN','constitutional_health_score':90}; x=build_governance_pulse(c,p); assert x['status']=='KRITIEKE WIJZIGING' and any(e['type']=='NEW_BLOCK' for e in x['executive_exception_feed'])

def test_debt_waiver_and_assurance_escalation():
 p={'decision_gate':'GO','active_waivers':1,'constitutional_debt_score':20,'open_migrations':0,'assurance_decision':'BEHOUDEN','constitutional_health_score':90}; c={'decision_gate':'GO','active_waivers':3,'constitutional_debt_score':35,'open_migrations':1,'assurance_decision':'HERSTELLEN','constitutional_health_score':82}; x=build_governance_pulse(c,p); types={e['type'] for e in x['executive_exception_feed']}; assert {'NEW_WAIVERS','DEBT_INCREASE','MIGRATION_DELAY','ASSURANCE_ESCALATION','HEALTH_DROP'} <= types
