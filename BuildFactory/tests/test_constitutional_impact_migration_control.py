from src.constitutional_impact_migration_control import analyze_constitutional_impact

V={'status':'AMENDMENT GECONTROLEERD VERWERKT','previous_version':'1.0','new_version':'2.0','applied_target':'GOVERNANCE_CONSTITUTION','current_version':{'version':'2.0'}}
def test_high_priority_blocks_activation():
 e={'mandates':[{'id':'M1','constitution_version':'1.0','financial_exposure_eur':5000}]}; x=analyze_constitutional_impact(V,e); assert x['status']=='ACTIVATIE GEBLOKKEERD - MIGRATIES VEREIST'; assert x['activation_ready'] is False
def test_completed_migration_allows_activation():
 e={'mandates':[{'id':'M1','constitution_version':'1.0','migration_complete':True}]}; x=analyze_constitutional_impact(V,e); assert x['status']=='ACTIVATIE GEREED'; assert x['activation_ready'] is True
def test_no_auto_activation():
 x=analyze_constitutional_impact(V,{}); assert x['automatic_activation'] is False and x['automatic_migration'] is False
