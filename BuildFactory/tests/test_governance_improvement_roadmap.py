from src.governance_improvement_roadmap import build_governance_improvement_roadmap

def test_no_actions_when_target_reached():
 x=build_governance_improvement_roadmap({'maturity_index':92,'domain_scores':{'governance':92,'finance':95}}); assert x['status']=='DOELNIVEAU BEREIKT'; assert x['action_count']==0

def test_large_gap_gets_36_month_horizon():
 x=build_governance_improvement_roadmap({'maturity_index':55,'domain_scores':{'audit':50}}); assert x['actions'][0]['horizon_months']==36; assert x['actions'][0]['target_score']==90

def test_existing_progress_is_preserved():
 first=build_governance_improvement_roadmap({'maturity_index':75,'domain_scores':{'treasury':70}}); rid=first['actions'][0]['roadmap_id']; existing={'actions':[{'roadmap_id':rid,'progress_percent':40,'status':'IN UITVOERING','owner':'Penningmeester VvE'}]}; x=build_governance_improvement_roadmap({'maturity_index':75,'domain_scores':{'treasury':70}},existing); assert x['actions'][0]['progress_percent']==40; assert x['actions'][0]['owner']=='Penningmeester VvE'
