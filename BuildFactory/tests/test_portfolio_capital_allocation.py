from src.portfolio_capital_allocation import allocate_portfolio_capital

PORTFOLIO={'ranking':[{'name':'A','risk_score':50,'reserve_per_apartment':5000,'lcc_per_apartment':20000,'sustainability_score':40,'closed_loop_score':60,'lcc_30_year':400000,'reserve':100000,'apartments':20,'rank':2},{'name':'B','risk_score':20,'reserve_per_apartment':15000,'lcc_per_apartment':12000,'sustainability_score':80,'closed_loop_score':90,'lcc_30_year':240000,'reserve':200000,'apartments':20,'rank':1}]}

def test_empty_portfolio():
    x=allocate_portfolio_capital({},100000); assert x['status']=='GEEN INVESTERINGSDATA'; assert x['unallocated_capital']==100000

def test_higher_priority_gets_capital_first():
    x=allocate_portfolio_capital(PORTFOLIO,150000); assert x['allocations'][0]['name']=='A'; assert x['allocations'][0]['allocated_capital']==150000; assert x['unallocated_capital']==0

def test_allocation_never_exceeds_available_capital():
    x=allocate_portfolio_capital(PORTFOLIO,500000); assert x['allocated_capital']<=500000; assert x['human_decision_required'] is True; assert x['automatic_commitment'] is False
