from src.vve_governance_operating_system import build_vve_governance_os

def healthy():
 return {'financial_cockpit':{'score':95},'mjop_engine':{'score':95},'risk_engine':{'risk_score':5},'portfolio_treasury_control_tower':{'treasury_score':95,'status':'GROEN'},'governance_maturity_index':{'maturity_index':95,'maturity_level':'LEIDEND'},'treasury_audit_assurance':{'overall_assurance_score':95},'treasury_accountability_register':{'accountability_score':95},'governance_improvement_roadmap':{'overall_progress':95}}

def test_green_integrated_os():
 x=build_vve_governance_os(healthy()); assert x['status']=='GROEN'; assert x['overall_vve_health_governance_score']>=90

def test_critical_treasury_blocks_green():
 r=healthy(); r['portfolio_treasury_control_tower']['treasury_score']=30; x=build_vve_governance_os(r); assert x['status']!='GROEN'; assert 'TREASURY' in x['critical_domains']

def test_returns_three_priorities():
 x=build_vve_governance_os({}); assert len(x['top_improvement_priorities'])==3; assert x['human_governance_preserved'] is True
