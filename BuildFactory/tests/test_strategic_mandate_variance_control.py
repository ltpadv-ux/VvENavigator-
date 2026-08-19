from src.strategic_mandate_variance_control import build_strategic_mandate_variance_control

MANDATE={'status':'STRATEGISCH MANDAAT ACTIEF','mandate':{'mandate_id':'PSM-1','contribution_path':[{'month':12,'contribution_delta':0.05},{'month':24,'contribution_delta':0.05},{'month':36,'contribution_delta':0.05}],'mjop_acceleration':0.10,'investment_budget_36m':100000,'kpi_targets':[{'month':12,'target_score':80},{'month':24,'target_score':85},{'month':36,'target_score':90}]}}

def test_no_active_mandate():
 x=build_strategic_mandate_variance_control({},{}); assert x['status']=='GEEN ACTIEF MANDAAT'

def test_green_on_track():
 a={'current_month':12,'contribution_delta':0.05,'mjop_acceleration':0.10,'investment_spend':80000,'governance_score':81,'evidence':['rapport']}
 x=build_strategic_mandate_variance_control(MANDATE,a); assert x['status']=='GROEN'

def test_red_on_budget_or_kpi_breach():
 a={'current_month':12,'contribution_delta':0.01,'mjop_acceleration':0.02,'investment_spend':120000,'governance_score':70,'evidence':['rapport']}
 x=build_strategic_mandate_variance_control(MANDATE,a); assert x['status']=='ROOD'; assert any(z['type']=='BUDGET' for z in x['alerts']); assert any(z['type']=='KPI' for z in x['alerts'])
