from src.board_decision_alv_financial_resolution_pack import build_financial_resolution_pack

def test_positive_pack():
 c={'cockpit_id':'C1','integrated_preferred_path':{'decision_path_id':'P1','scenario_name':'GEBALANCEERD','term_months':36,'reserve_share_pct':25,'integrated_decision_score':86,'reserve_floor_ok':True,'mjop_buffer_ok':True,'blocker':False},'ranked_integrated_paths':[]}; x=build_financial_resolution_pack(c); assert x['recommendation']=='VOORLEGGEN MET POSITIEF ADVIES' and 'ALV besluit' in x['draft_alv_resolution']
def test_blocked_pack_requires_recalibration():
 c={'integrated_preferred_path':{'decision_path_id':'P1','integrated_decision_score':90,'reserve_floor_ok':False,'mjop_buffer_ok':True,'blocker':True},'ranked_integrated_paths':[]}; assert build_financial_resolution_pack(c)['recommendation']=='NIET VOORLEGGEN ZONDER HERIJKING'
def test_no_automatic_adoption():
 c={'integrated_preferred_path':{'decision_path_id':'P1','integrated_decision_score':80,'reserve_floor_ok':True,'mjop_buffer_ok':True,'blocker':False}}; x=build_financial_resolution_pack(c); assert x['automatic_resolution_adoption'] is False and x['automatic_decision'] is False
