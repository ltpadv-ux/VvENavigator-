from src.constitutional_compliance_gatekeeper import evaluate_decision_gate

C={'constitution_id':'C1','status':'VASTGESTELD','authority_matrix':{'Bestuur':['beheer'],'ALV':['begroting']}}
def test_go():
 p={'proposal_id':'P1','decision_authority':'Bestuur','financial_commitment_eur':1000,'approved_budget_eur':1000,'risk_level':'GROEN','audit_trail_complete':True,'explainability_complete':True}; assert evaluate_decision_gate(p,C)['gate']=='GO'
def test_block_budget():
 p={'decision_authority':'Bestuur','financial_commitment_eur':2000,'approved_budget_eur':1000,'audit_trail_complete':True,'explainability_complete':True}; assert evaluate_decision_gate(p,C)['gate']=='BLOCK'
def test_review_red_risk():
 p={'decision_authority':'Bestuur','financial_commitment_eur':500,'approved_budget_eur':1000,'risk_level':'ROOD','audit_trail_complete':True,'explainability_complete':True}; assert evaluate_decision_gate(p,C)['gate']=='REVIEW'
