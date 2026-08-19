from src.predictive_board_mandate import build_predictive_board_mandate

PORTFOLIO={'board_choice_cards':[{'label':'LAAGSTE KOSTEN','pareto_rank':1,'intervention':{'contribution_delta':0.03,'mjop_acceleration':0.05,'financing_share':0.25,'sustainability_investment':0.1},'score_12m':72,'score_24m':76,'score_36m':80,'estimated_36m_cost':125000,'risk_reduction':7,'sustainability_impact':10}]}

def test_requires_board_approval():
 x=build_predictive_board_mandate(PORTFOLIO); assert x['status']=='BESLUIT VEREIST'; assert x['mandate']=={}

def test_approved_choice_creates_mandate():
 existing={'decision':{'selected_label':'LAAGSTE KOSTEN','decision':'GOEDGEKEURD','approved_by':'ALV'}}
 x=build_predictive_board_mandate(PORTFOLIO,existing); assert x['status']=='STRATEGISCH MANDAAT ACTIEF'; assert x['mandate']['mandate_id'].startswith('PSM-'); assert x['mandate']['investment_budget_36m']==125000

def test_kpi_targets_cover_12_24_36_months():
 existing={'decision':{'decision':'AKKOORD','approved_by':'Bestuur'}}
 x=build_predictive_board_mandate(PORTFOLIO,existing); assert [k['month'] for k in x['mandate']['kpi_targets']]==[12,24,36]; assert x['automatic_execution'] is False
