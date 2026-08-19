from src.governance_maturity_index import build_governance_maturity_index

def test_high_maturity():
 r={'closed_loop_management':{'loop_completeness_score':95},'financial_cockpit':{'score':95},'mjop_engine':{'score':90},'portfolio_treasury_control_tower':{'treasury_score':95},'treasury_audit_assurance':{'overall_assurance_score':95},'treasury_accountability_register':{'accountability_score':95},'audit_remediation':{'open_count':0}}
 x=build_governance_maturity_index(r); assert x['maturity_level']=='LEIDEND'; assert x['maturity_index']>=90

def test_open_remediation_reduces_index():
 base={'closed_loop_management':{'loop_completeness_score':80},'financial_cockpit':{'score':80},'mjop_engine':{'score':80},'portfolio_treasury_control_tower':{'treasury_score':80},'treasury_audit_assurance':{'overall_assurance_score':80},'treasury_accountability_register':{'accountability_score':80}}
 a=build_governance_maturity_index({**base,'audit_remediation':{'open_count':0}}); b=build_governance_maturity_index({**base,'audit_remediation':{'open_count':3}}); assert b['maturity_index']<a['maturity_index']

def test_weakest_domains_returned():
 x=build_governance_maturity_index({'portfolio_treasury_control_tower':{'treasury_score':20}}); assert len(x['weakest_domains'])==3
