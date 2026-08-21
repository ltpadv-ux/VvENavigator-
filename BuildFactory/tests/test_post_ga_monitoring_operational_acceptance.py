from src.post_ga_monitoring_operational_acceptance import evaluate_post_ga_operations

def test_healthy_post_ga_is_operationally_accepted():
 x=evaluate_post_ga_operations({'ga_release_completed':True},{'periods_observed':3,'critical_incidents':0,'availability_pct':99.9,'error_rate_pct':0.2,'rollback_signal':False,'data_integrity_ok':True},{'operations_owner_approved':True,'business_owner_approved':True}); assert x['status']=='OPERATIONALLY ACCEPTED' and x['steady_state_operations_allowed'] is True
def test_critical_incident_requires_rollback_review():
 x=evaluate_post_ga_operations({'ga_release_completed':True},{'periods_observed':3,'critical_incidents':1,'availability_pct':99.9,'error_rate_pct':0.2,'rollback_signal':False,'data_integrity_ok':True},{'operations_owner_approved':True,'business_owner_approved':True}); assert x['requires_rollback_review'] is True and x['status']=='POST-GA NO-GO / ROLLBACK REVIEW'
def test_insufficient_monitoring_holds_and_never_auto_accepts():
 x=evaluate_post_ga_operations({'ga_release_completed':True},{'periods_observed':1,'critical_incidents':0,'availability_pct':99.9,'error_rate_pct':0.2,'rollback_signal':False,'data_integrity_ok':True},{'operations_owner_approved':True,'business_owner_approved':True}); assert x['status']=='POST-GA HOLD - ACCEPTANCE PENDING' and x['automatic_acceptance'] is False
