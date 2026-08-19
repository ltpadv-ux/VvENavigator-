from src.constitutional_remediation_amendment_register import register_remediation_amendment
R={'debt_level':'ROOD','debt_score':80,'constitutional_debt_remediation_version':'12.4.0','actions':[{'type':'CONSTITUTION_REBASELINE','scope':'constitution','financial_impact_eur':10000}]}
def test_approved_amendment():
 d={'action_type':'CONSTITUTION_REBASELINE','approval_status':'AANGENOMEN','decision_authority':'ALV','rationale':'Structurele herijking nodig','resolution_reference':'ALV-2026-12','effective_date':'2026-09-01','review_date':'2027-09-01','target_version':'2.0'}; x=register_remediation_amendment(R,d,{'constitution_id':'C1','version':'1.0'}); assert x['ready_for_controlled_processing'] is True and x['amendment']['target']=='GOVERNANCE_CONSTITUTION'
def test_missing_resolution_is_incomplete():
 d={'action_type':'CONSTITUTION_REBASELINE','approval_status':'AANGENOMEN','decision_authority':'ALV','rationale':'Herijking','review_date':'2027-01-01'}; assert register_remediation_amendment(R,d)['ready_for_controlled_processing'] is False
def test_no_automatic_application():
 x=register_remediation_amendment(R,{}); assert x['automatic_amendment_application'] is False and x['automatic_constitution_change'] is False
