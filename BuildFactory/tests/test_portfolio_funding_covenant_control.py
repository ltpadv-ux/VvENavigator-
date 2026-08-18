from src.portfolio_funding_covenant_control import build_funding_decision_and_covenants

STRATEGY={'assumptions':{'loan_rate':0.04},'strategies':[{'name':'VvE A','funding_gap':100000,'preferred_scenario':'RESERVE + LENING','scenarios':[{'scenario':'RESERVE + LENING','reserve_use':25000,'loan_amount':75000,'monthly_cost_per_apartment':55}]}]}

def test_pending_human_decision():
    x=build_funding_decision_and_covenants(STRATEGY); assert x['status']=='BESLUIT VEREIST'; assert x['pending_count']==1; assert x['automatic_financing_commitment'] is False

def test_approved_mix_within_covenants():
    first=build_funding_decision_and_covenants(STRATEGY); did=first['decisions'][0]['decision_id']; existing={'decisions':[{'decision_id':did,'selected_scenario':'RESERVE + LENING','decision':'GOEDGEKEURD','approved_by':'ALV'}]}
    x=build_funding_decision_and_covenants(STRATEGY,existing); assert x['status']=='FINANCIERING GEBORGD'; assert x['approved_count']==1

def test_covenant_breach_blocks_financing():
    bad={'assumptions':{'loan_rate':0.07},'strategies':[{'name':'VvE B','funding_gap':100000,'preferred_scenario':'LENING','scenarios':[{'scenario':'LENING','reserve_use':0,'loan_amount':100000,'monthly_cost_per_apartment':95}]}]}
    x=build_funding_decision_and_covenants(bad); assert x['status']=='COVENANT BREACH'; assert x['breach_count']>=1
