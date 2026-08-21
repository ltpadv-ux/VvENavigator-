"""Enterprise 17.0 Security, Access Control & Release Hardening Gate."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='17.0.0'
REQUIRED_CONTROLS=('rbac','least_privilege','secrets_management','audit_logging','dependency_scan','vulnerability_scan','backup_restore_verified','ci_evidence_gate','release_notes','human_release_signoff')
def _id(*parts:Any)->str:return 'GOVSEC-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def evaluate_security_release_gate(controls:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; required=tuple(rules.get('required_controls',REQUIRED_CONTROLS)); rows=[]; blockers=[]
 for name in required:
  raw=controls.get(name,{})
  if isinstance(raw,dict): passed=bool(raw.get('passed',False)); evidence=raw.get('evidence_ref'); note=raw.get('note')
  else: passed=bool(raw); evidence=None; note=None
  rows.append({'control':name,'passed':passed,'evidence_ref':evidence,'note':note})
  if not passed:blockers.append(f'SECURITY_CONTROL_FAIL:{name}')
 critical_vulns=int(controls.get('critical_vulnerabilities',0) or 0); high_vulns=int(controls.get('high_vulnerabilities',0) or 0); exposed_secrets=int(controls.get('exposed_secrets',0) or 0)
 if critical_vulns>int(rules.get('max_critical_vulnerabilities',0)):blockers.append('CRITICAL_VULNERABILITIES_PRESENT')
 if high_vulns>int(rules.get('max_high_vulnerabilities',0)):blockers.append('HIGH_VULNERABILITIES_PRESENT')
 if exposed_secrets>0:blockers.append('EXPOSED_SECRETS_PRESENT')
 privileged_accounts=int(controls.get('privileged_accounts',0) or 0); mfa_privileged=int(controls.get('privileged_accounts_with_mfa',0) or 0)
 mfa_ok=(privileged_accounts==mfa_privileged) if privileged_accounts else True
 if not mfa_ok:blockers.append('PRIVILEGED_MFA_INCOMPLETE')
 evidence_complete=all(r['evidence_ref'] for r in rows if r['passed'])
 if bool(rules.get('require_evidence_for_passed_controls',True)) and not evidence_complete:blockers.append('SECURITY_EVIDENCE_INCOMPLETE')
 ready=not blockers
 return {'security_access_release_hardening_gate_version':ENGINE_VERSION,'security_gate_id':_id(len(required),critical_vulns,high_vulns,exposed_secrets),'status':'SECURITY & RELEASE HARDENING PASSED' if ready else 'SECURITY & RELEASE HARDENING BLOCKED','control_results':rows,'critical_vulnerabilities':critical_vulns,'high_vulnerabilities':high_vulns,'exposed_secrets':exposed_secrets,'privileged_accounts':privileged_accounts,'privileged_accounts_with_mfa':mfa_privileged,'privileged_mfa_complete':mfa_ok,'evidence_complete':evidence_complete,'blockers':blockers,'production_security_ready':ready,'requires_security_owner_approval':ready,'requires_release_owner_approval':ready,'automatic_release':False,'automatic_access_change':False,'automatic_secret_rotation':False,'automatic_vulnerability_acceptance':False,'next_action':'Laat security owner en release owner het evidence pack expliciet goedkeuren.' if ready else 'Herstel security/release blockers, voeg bewijs toe en voer de hardening gate opnieuw uit.'}
