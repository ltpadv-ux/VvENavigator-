from src.preventive_governance_intervention_planner import build_preventive_governance_plan

def test_plan_created_for_near_threshold():
 f={'status':'ROOD/ORANJE BINNEN 3 RUNS','forecast_horizon_runs':2,'threshold_forecast_runs':{'debt_orange':2,'debt_red':6,'health_orange':None,'health_red':None,'waiver_pressure':2,'migration_pressure':None,'assurance_escalation':None}}
 c={'tower_id':'T1','constitutional_debt_score':35,'constitutional_health_score':82,'active_waivers':2,'open_migrations':0}; x=build_preventive_governance_plan(f,c); assert x['status']=='PREVENTIEF INTERVENTIEPLAN VEREIST' and x['action_count']>=2

def test_no_plan_when_no_threshold_near():
 f={'forecast_horizon_runs':8,'threshold_forecast_runs':{'debt_orange':8,'debt_red':12}}; x=build_preventive_governance_plan(f,{'constitutional_health_score':90}); assert x['action_count']==0

def test_no_automatic_execution():
 x=build_preventive_governance_plan({'threshold_forecast_runs':{}},{}); assert x['automatic_intervention'] is False and x['automatic_execution'] is False
