from src.executive_command_center import build_executive_command_center

def test_empty_report_is_on_course():
 x=build_executive_command_center({}); assert x['board_status']=='OP KOERS'; assert x['automatic_decision'] is False

def test_critical_recommendation_requires_direct_decision():
 r={'autonomous_governance_recommendation':{'recommendations':[{'priority':'KRITIEK','topic':'liquidity'}]}}
 x=build_executive_command_center(r); assert x['board_status']=='DIRECT BESLUIT VEREIST'; assert x['critical_action_count']==1

def test_integrates_core_scores():
 r={'vve_governance_operating_system':{'overall_vve_health_governance_score':82,'status':'ORANJE'},'portfolio_treasury_control_tower':{'treasury_score':77},'treasury_audit_assurance':{'overall_assurance_score':88},'governance_maturity_index':{'maturity_index':84},'executive_digital_twin':{'best_36m_scenario':'BALANS','best_36m_score':90}}
 x=build_executive_command_center(r); s=x['executive_summary']; assert s['health_governance_score']==82; assert s['treasury_score']==77; assert s['best_36m_scenario']=='BALANS'
