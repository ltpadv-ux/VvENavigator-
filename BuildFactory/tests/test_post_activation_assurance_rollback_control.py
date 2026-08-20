from src.post_activation_assurance_rollback_control import assess_post_activation
C={'status':'CUTOVER GEREED VOOR FORMELE ACTIVATIE','cutover':{'cutover_id':'CUT1','new_version':'2.0','rollback_version':'1.0'}}
def test_keep_when_stable():
 x=assess_post_activation(C,{'activated':True,'compliance_score':95,'kpi_stability_score':92}); assert x['decision']=='BEHOUDEN'
def test_repair_when_kpi_unstable():
 x=assess_post_activation(C,{'activated':True,'compliance_score':90,'kpi_stability_score':70,'migration_issues':1}); assert x['decision']=='HERSTELLEN'
def test_rollback_when_critical():
 x=assess_post_activation(C,{'activated':True,'compliance_score':55,'kpi_stability_score':60,'critical_incidents':2}); assert x['decision']=='ROLLBACK' and x['automatic_rollback'] is False
