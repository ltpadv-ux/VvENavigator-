from src.intervention_execution_mandate import build_intervention_execution_mandate

MATRIX={'ranking':[{'rank':1,'intervention_id':'INT-001','domain':'RISICO','kpi':'12-maands risicodruk','option':'Versnel kritieke MJOP-maatregelen','decision_authority':'Bestuur/ALV','weighted_score':91.5,'impact':{'projected_reserve':180000,'monthly_contribution_per_apartment':225,'mjop_shift_months':-6,'risk_score_delta':-12,'horizons':{'30':{'lcc':60000}}}}]}

def test_requires_human_decision():
    x=build_intervention_execution_mandate(MATRIX); assert x['status']=='BESLUIT VEREIST'; assert x['mandate']=={}; assert x['automatic_execution'] is False

def test_approved_decision_creates_mandate():
    existing={'decision':{'selected_option':'Versnel kritieke MJOP-maatregelen','decision':'GOEDGEKEURD','approved_by':'ALV','rationale':'Beste totaalscore'}}
    x=build_intervention_execution_mandate(MATRIX,existing); assert x['status']=='MANDAAT ACTIEF'; assert x['mandate']['mandate_id'].startswith('INTMAN-'); assert x['mandate']['budget_ceiling']==60000; assert x['mandate']['effect_measurement_required'] is True

def test_existing_owner_and_deadline_are_preserved():
    existing={'decision':{'selected_option':'Versnel kritieke MJOP-maatregelen','decision':'GOEDGEKEURD','approved_by':'Bestuur'},'mandate':{'owner':'Technisch beheerder','execution_deadline':'2027-06-30'}}
    x=build_intervention_execution_mandate(MATRIX,existing); assert x['mandate']['owner']=='Technisch beheerder'; assert x['mandate']['execution_deadline']=='2027-06-30'
