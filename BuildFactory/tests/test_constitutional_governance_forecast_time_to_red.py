from src.constitutional_governance_forecast_time_to_red import forecast_governance_time_to_red

def test_no_red_path_when_stable():
 r={'trend_metrics':{'debt_slope':0,'health_slope':0,'waiver_slope':0,'migration_slope':0,'assurance_slope':0}}
 c={'constitutional_debt_score':10,'constitutional_health_score':95,'active_waivers':0,'open_migrations':0,'assurance_decision':'BEHOUDEN'}
 x=forecast_governance_time_to_red(r,c); assert x['status']=='GEEN ROODPAD GEPROJECTEERD'

def test_debt_forecast_detected():
 r={'trend_metrics':{'debt_slope':10,'health_slope':0,'waiver_slope':0,'migration_slope':0,'assurance_slope':0}}
 c={'constitutional_debt_score':50,'constitutional_health_score':90,'active_waivers':0,'open_migrations':0,'assurance_decision':'BEHOUDEN'}
 x=forecast_governance_time_to_red(r,c); assert x['threshold_forecast_runs']['debt_red']==2 and x['human_board_review_required'] is True

def test_health_forecast_detected():
 r={'trend_metrics':{'debt_slope':0,'health_slope':-5,'waiver_slope':0,'migration_slope':0,'assurance_slope':0}}
 c={'constitutional_debt_score':10,'constitutional_health_score':80,'active_waivers':0,'open_migrations':0,'assurance_decision':'BEHOUDEN'}
 x=forecast_governance_time_to_red(r,c); assert x['threshold_forecast_runs']['health_orange']==2
