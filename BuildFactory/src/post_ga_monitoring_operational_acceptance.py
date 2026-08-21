"""Enterprise 18.3 Post-GA Monitoring & Operational Acceptance."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='18.3.0'
def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0
def _id(*p:Any)->str:return 'GOVOPS-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:12].upper()
def evaluate_post_ga_operations(release_record:dict[str,Any], monitoring:dict[str,Any], approvals:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; released=bool(release_record.get('ga_release_completed',False)); periods=int(monitoring.get('periods_observed',0) or 0); incidents=int(monitoring.get('critical_incidents',0) or 0); availability=_n(monitoring.get('availability_pct')); error_rate=_n(monitoring.get('error_rate_pct')); rollback=bool(monitoring.get('rollback_signal',False)); data_integrity=bool(monitoring.get('data_integrity_ok',False)); kpi_ok=availability>=_n(rules.get('minimum_availability_pct',99.5)) and error_rate<=_n(rules.get('maximum_error_rate_pct',1.0)); min_periods=int(rules.get('minimum_monitoring_periods',3)); ops_approved=bool(approvals.get('operations_owner_approved',False)); business_approved=bool(approvals.get('business_owner_approved',False)); blockers=[]
 if not released:blockers.append('GA_RELEASE_NOT_COMPLETED')
 if periods<min_periods:blockers.append('INSUFFICIENT_MONITORING_PERIODS')
 if incidents>0:blockers.append('CRITICAL_INCIDENTS_PRESENT')
 if not kpi_ok:blockers.append('OPERATIONAL_KPI_BREACH')
 if rollback:blockers.append('ROLLBACK_SIGNAL_ACTIVE')
 if not data_integrity:blockers.append('DATA_INTEGRITY_NOT_CONFIRMED')
 if not ops_approved:blockers.append('OPERATIONS_OWNER_APPROVAL_MISSING')
 if not business_approved:blockers.append('BUSINESS_OWNER_APPROVAL_MISSING')
 critical={'GA_RELEASE_NOT_COMPLETED','CRITICAL_INCIDENTS_PRESENT','ROLLBACK_SIGNAL_ACTIVE','DATA_INTEGRITY_NOT_CONFIRMED'}; critical_blockers=[b for b in blockers if b in critical]
 status='OPERATIONALLY ACCEPTED' if not blockers else ('POST-GA NO-GO / ROLLBACK REVIEW' if critical_blockers else 'POST-GA HOLD - ACCEPTANCE PENDING')
 return {'post_ga_monitoring_operational_acceptance_version':ENGINE_VERSION,'operational_acceptance_id':_id(status,periods,incidents,availability,error_rate),'status':status,'periods_observed':periods,'availability_pct':availability,'error_rate_pct':error_rate,'critical_incidents':incidents,'data_integrity_ok':data_integrity,'rollback_signal':rollback,'operational_kpis_within_gate':kpi_ok,'blockers':blockers,'critical_blockers':critical_blockers,'operational_acceptance_granted':status=='OPERATIONALLY ACCEPTED','steady_state_operations_allowed':status=='OPERATIONALLY ACCEPTED','requires_rollback_review':bool(critical_blockers),'automatic_rollback':False,'automatic_acceptance':False,'next_action':'Draag over naar steady-state operations en blijf periodiek monitoren.' if status=='OPERATIONALLY ACCEPTED' else ('Voer rollback/incident review uit vóór verdere operationele acceptatie.' if critical_blockers else 'Voltooi monitoringperiode, herstel KPI-gaps en verzamel ontbrekende approvals.')}
