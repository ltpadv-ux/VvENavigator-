from src.executive_decision_pulse import build_executive_decision_pulse

def command(status='OP KOERS',score=80,actions=None):
 return {'board_status':status,'executive_summary':{'health_governance_score':score,'financial_health':80,'mjop_health':80,'risk_score':20,'treasury_score':80,'audit_assurance':80,'governance_maturity':80,'best_36m_score':85,'downside_36m_score':70},'top_board_actions':actions or [],'critical_action_count':sum(1 for a in (actions or []) if a.get('priority')=='KRITIEK')}

def test_stable_when_no_material_change():
 cur=command(); prev=command(); x=build_executive_decision_pulse(cur,prev,'2026-08-19T12:00:00Z'); assert x['pulse_status']=='STABIEL'; assert x['board_status_changed'] is False

def test_new_critical_action_flags_critical_change():
 action={'recommendation_id':'GRA-1','topic':'liquidity','priority':'KRITIEK'}; cur=command('DIRECT BESLUIT VEREIST',70,[action]); prev=command('OP KOERS',80,[]); x=build_executive_decision_pulse(cur,prev); assert x['pulse_status']=='KRITIEKE WIJZIGING'; assert x['new_action_count']==1

def test_risk_decrease_shows_positive_trend():
 prev=command(); cur=command(); prev['executive_summary']['risk_score']=30; cur['executive_summary']['risk_score']=20; x=build_executive_decision_pulse(cur,prev); risk=next(r for r in x['kpi_changes'] if r['kpi']=='risk_score'); assert risk['trend']=='↑'
