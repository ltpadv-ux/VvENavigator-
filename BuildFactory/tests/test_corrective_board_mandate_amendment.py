from src.corrective_board_mandate_amendment import build_corrective_board_mandate_amendment

BOARD={'mandate':{'mandate_id':'PSM-1','status':'ACTIEF','mjop_acceleration':0.10,'sustainability_investment':0.20,'investment_budget_36m':100000,'contribution_path':[{'month':12,'contribution_delta':0.05},{'month':24,'contribution_delta':0.05},{'month':36,'contribution_delta':0.05}],'kpi_targets':[{'month':12,'target_score':70},{'month':24,'target_score':75},{'month':36,'target_score':80}]}}
OPT={'ranking':[{'rank':1,'action':{'extra_contribution_delta':0.02,'extra_mjop_acceleration':0.05,'budget_reduction_pct':0.10,'sustainability_adjustment':0.05},'projected_governance_score':82,'estimated_corrective_cost':15000}]}

def test_requires_board_decision():
 x=build_corrective_board_mandate_amendment(OPT,BOARD); assert x['status']=='BESLUIT VEREIST'; assert x['amendment']=={}

def test_approved_action_amends_mandate():
 existing={'decision':{'selected_rank':1,'decision':'GOEDGEKEURD','approved_by':'ALV','rationale':'Herstel op koers'}}
 x=build_corrective_board_mandate_amendment(OPT,BOARD,existing); assert x['status']=='MANDAATWIJZIGING GOEDGEKEURD'; assert x['amended_mandate']['mjop_acceleration']==0.15; assert x['amended_mandate']['contribution_path'][0]['contribution_delta']==0.07; assert x['amendment']['amendment_id'].startswith('PSMA-')

def test_history_is_preserved_without_duplicate():
 existing={'decision':{'selected_rank':1,'decision':'GOEDGEKEURD','approved_by':'Bestuur'}}
 first=build_corrective_board_mandate_amendment(OPT,BOARD,existing); again=build_corrective_board_mandate_amendment(OPT,BOARD,{**first,'decision':first['decision'],'amendment':first['amendment'],'amendment_history':first['amendment_history']}); assert len(again['amendment_history'])==1
