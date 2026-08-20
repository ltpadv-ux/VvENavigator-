from src.constitutional_governance_trend_drift_radar import analyze_governance_trend

def test_insufficient_history():
 x=analyze_governance_trend([{'constitutional_debt_score':10}]*3); assert x['status']=='ONVOLDOENDE HISTORIE'
def test_detects_drift():
 p=[{'constitutional_debt_score':10+i*5,'active_waivers':i,'open_migrations':i,'constitutional_health_score':95-i*3,'assurance_decision':'BEHOUDEN' if i<3 else 'HERSTELLEN'} for i in range(5)]; x=analyze_governance_trend(p); assert x['drift_level'] in {'ORANJE','ROOD'} and x['early_drift_alerts']
def test_no_automatic_decision():
 p=[{'constitutional_debt_score':0,'active_waivers':0,'open_migrations':0,'constitutional_health_score':95,'assurance_decision':'BEHOUDEN'} for _ in range(4)]; x=analyze_governance_trend(p); assert x['automatic_decision'] is False and x['automatic_execution'] is False
