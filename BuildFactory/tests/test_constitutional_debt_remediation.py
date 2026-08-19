from src.constitutional_debt_remediation import build_constitutional_debt_remediation

def test_green_debt_needs_no_plan():
 x=build_constitutional_debt_remediation({'constitutional_debt_level':'GROEN','constitutional_debt_score':0}); assert x['status']=='GEEN FORMELE REMEDIATION NODIG'

def test_orange_repeated_exception_creates_doctrine_review():
 d={'constitutional_debt_level':'ORANJE','constitutional_debt_score':55,'repeated_exception_patterns':[{'scope':'MJOP','count':3,'financial_impact_eur':12000}]}; x=build_constitutional_debt_remediation(d); assert any(a['type']=='NORMALIZE_REPEATED_EXCEPTION' for a in x['actions']); assert any(a['type']=='DOCTRINE_REVIEW' for a in x['actions'])

def test_red_debt_creates_constitution_rebaseline():
 d={'constitutional_debt_level':'ROOD','constitutional_debt_score':80,'total_financial_impact_eur':50000,'expired_waivers':1}; x=build_constitutional_debt_remediation(d,{'constitution_id':'C1'}); assert any(a['type']=='CONSTITUTION_REBASELINE' for a in x['actions']); assert x['automatic_constitution_change'] is False
