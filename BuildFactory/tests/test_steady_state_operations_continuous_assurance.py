from src.steady_state_operations_continuous_assurance import evaluate_continuous_assurance

def _controls(): return {'backup_recent':True,'restore_test_current':True,'security_scan_current':True,'audit_log_integrity':True,'data_integrity_verified':True,'access_review_current':True}
def _approvals(): return {'operations_owner_approved':True,'security_owner_approved':True,'business_owner_approved':True}
def test_green_steady_state_is_accepted():
 x=evaluate_continuous_assurance({'assurance_periods':3,'availability_pct':99.9,'error_rate_pct':0.2,'critical_incidents':0},_controls(),_approvals()); assert x['steady_state_accepted'] is True and x['continuous_assurance_green'] is True
def test_failed_control_blocks_assurance():
 c=_controls(); c['security_scan_current']=False; x=evaluate_continuous_assurance({'assurance_periods':3,'availability_pct':99.9,'error_rate_pct':0.2},c,_approvals()); assert x['requires_corrective_action'] is True and 'CONTROL_FAIL:security_scan_current' in x['blockers']
def test_critical_incident_escalates():
 x=evaluate_continuous_assurance({'assurance_periods':3,'availability_pct':99.9,'error_rate_pct':0.2,'critical_incidents':1},_controls(),_approvals()); assert x['requires_board_escalation'] is True and x['automatic_corrective_action'] is False
