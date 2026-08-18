from src.portfolio_intelligence import build_portfolio_intelligence

def sample(reserve,risk,loop):
    return {'release':{'dashboard':{'reserve':reserve,'risk_score':risk},'executive_cockpit':{'key_metrics':{'apartments':10,'monthly_per_apartment':200,'lcc_30_year':300000}}},'closed_loop_management':{'loop_completeness_score':loop,'governance_safe':True},'execution_benefits_tracking':{'benefits':{'realization_score':80}}}

def test_empty_portfolio():
    x=build_portfolio_intelligence([]); assert x['portfolio_count']==0

def test_benchmark_and_ranking():
    x=build_portfolio_intelligence([('A',sample(200000,10,100)),('B',sample(100000,40,60))]); assert x['portfolio_count']==2; assert x['ranking'][0]['name']=='A'; assert x['benchmarks']['reserve_per_apartment']['median']==15000

def test_priority_prefers_higher_risk():
    x=build_portfolio_intelligence([('A',sample(200000,10,100)),('B',sample(100000,40,60))]); assert x['priority_vves'][0]=='B'
