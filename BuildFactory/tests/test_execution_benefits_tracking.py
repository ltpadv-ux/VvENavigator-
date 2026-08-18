from src.execution_benefits_tracking import track_execution_and_benefits

EXEC={'status':'MANDAAT ACTIEF','mandate':{'mandate_id':'INTMAN-1','owner':'Technisch beheerder','budget_ceiling':60000,'projected_reserve':180000,'monthly_contribution_per_apartment':225,'target_risk_delta':-12,'mjop_shift_months':-6,'execution_deadline':'2099-12-31'}}
REPORT={'governance_control_tower':{'kpis':{'reserve':180000,'monthly_per_apartment':220}}}

def test_active_mandate_starts_tracking():
    x=track_execution_and_benefits(EXEC,REPORT); assert x['status']=='IN UITVOERING'; assert x['tracking']['budget_remaining']==60000

def test_completed_execution_without_effect_stays_open():
    state={'tracking':{'progress_percent':100,'spent_amount':50000,'actual_risk_delta':-5,'actual_mjop_shift_months':-6}}
    x=track_execution_and_benefits(EXEC,REPORT,state); assert x['closure']['status']=='OPEN'; assert x['status']=='EFFECTCONTROLE'

def test_completed_execution_with_effect_closes():
    state={'tracking':{'progress_percent':100,'spent_amount':50000,'actual_risk_delta':-12,'actual_mjop_shift_months':-6}}
    x=track_execution_and_benefits(EXEC,REPORT,state); assert x['closure']['status']=='GESLOTEN'; assert x['benefits']['realization_score']==100.0
