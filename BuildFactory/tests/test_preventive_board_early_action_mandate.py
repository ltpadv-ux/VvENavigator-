from src.preventive_board_early_action_mandate import build_preventive_board_early_action_mandate

def sim():
 return {'status':'IMPACT PREVIEW BESCHIKBAAR','trigger_alert_count':2,'avoided_recovery_cost':32000,'recommended_scenario':{'scenario':'VROEG INGRIJPEN','estimated_cost':18000,'projected_health_score':84,'projected_risk_score':28,'horizon_months':12},'scenarios':[{'scenario':'VROEG INGRIJPEN','estimated_cost':18000,'projected_health_score':84,'projected_risk_score':28,'horizon_months':12}]}

def test_requires_board_decision():
 x=build_preventive_board_early_action_mandate(sim()); assert x['status']=='BESLUIT VEREIST'; assert x['automatic_execution'] is False

def test_approved_creates_active_mandate():
 e={'decision':{'decision':'GOEDGEKEURD','approved_by':'ALV'}}; x=build_preventive_board_early_action_mandate(sim(),e); assert x['status']=='VROEG-ACTIEMANDAAT ACTIEF'; assert x['mandate']['mandate_id'].startswith('PEAM-'); assert x['mandate']['budget']==18000

def test_existing_execution_fields_preserved():
 e={'decision':{'decision':'GOEDGEKEURD'},'mandate':{'owner':'Penningmeester','progress_pct':40,'actual_spend':5000,'evidence':['offerte']}}
 x=build_preventive_board_early_action_mandate(sim(),e); assert x['mandate']['owner']=='Penningmeester'; assert x['mandate']['progress_pct']==40; assert x['mandate']['evidence']==['offerte']
