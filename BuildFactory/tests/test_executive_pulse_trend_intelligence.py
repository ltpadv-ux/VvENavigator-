from src.executive_pulse_trend_intelligence import build_pulse_trend_intelligence

def pulse(at,health=80,risk=20):
 return {'run_at':at,'board_status':'OP KOERS','pulse_status':'STABIEL','kpi_changes':[{'kpi':'health_governance_score','current':health},{'kpi':'risk_score','current':risk}]}

def test_history_accumulates():
 a=build_pulse_trend_intelligence(pulse('1',80)); b=build_pulse_trend_intelligence(pulse('2',82),a); assert b['history_count']==2

def test_improving_health_detected():
 x={};
 for i,v in enumerate([70,75,80],1): x=build_pulse_trend_intelligence(pulse(str(i),v),x)
 assert x['domain_trends']['health_governance_score']['trend']=='VERBETERT'

def test_risk_decline_is_improvement():
 x={};
 for i,v in enumerate([30,25,20],1): x=build_pulse_trend_intelligence(pulse(str(i),80,v),x)
 assert x['domain_trends']['risk_score']['trend']=='VERBETERT'
