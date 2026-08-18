from src.portfolio_funding_strategy import build_portfolio_funding_strategy

def test_no_gap_requires_no_financing():
    allocation={'allocations':[{'name':'A','funding_gap':0}]}
    x=build_portfolio_funding_strategy(allocation)
    assert x['status']=='GEEN FINANCIERINGSGATEN'

def test_gap_creates_ranked_financing_scenarios():
    allocation={'allocations':[{'name':'A','funding_gap':120000,'priority_score':88,'apartments':40}]}
    x=build_portfolio_funding_strategy(allocation,{'loan_rate':0.04,'loan_years':15,'subsidy_rate':0.10})
    assert x['status']=='FINANCIERINGSSTRATEGIE BESCHIKBAAR'
    assert len(x['strategies'][0]['scenarios'])==4
    assert x['strategies'][0]['scenarios'][0]['rank']==1

def test_human_governance_is_preserved():
    allocation={'allocations':[{'name':'A','funding_gap':50000,'priority_score':70}]}
    x=build_portfolio_funding_strategy(allocation)
    assert x['human_decision_required'] is True
    assert x['automatic_financing_commitment'] is False
