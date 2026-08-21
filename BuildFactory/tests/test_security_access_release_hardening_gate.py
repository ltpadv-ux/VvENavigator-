from src.security_access_release_hardening_gate import evaluate_security_release_gate,REQUIRED_CONTROLS

def _ok(): return {c:{'passed':True,'evidence_ref':f'ev-{c}'} for c in REQUIRED_CONTROLS}
def test_full_security_gate_passes():
 c=_ok(); c.update({'privileged_accounts':2,'privileged_accounts_with_mfa':2}); x=evaluate_security_release_gate(c); assert x['production_security_ready'] is True
def test_exposed_secret_blocks():
 c=_ok(); c['exposed_secrets']=1; x=evaluate_security_release_gate(c); assert x['production_security_ready'] is False and 'EXPOSED_SECRETS_PRESENT' in x['blockers']
def test_missing_privileged_mfa_blocks():
 c=_ok(); c.update({'privileged_accounts':2,'privileged_accounts_with_mfa':1}); x=evaluate_security_release_gate(c); assert x['privileged_mfa_complete'] is False and x['automatic_release'] is False
