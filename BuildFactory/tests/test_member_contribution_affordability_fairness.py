from src.member_contribution_affordability_fairness import assess_member_affordability_fairness

def test_average_apartment_affordability():
 f={'funding_id':'F1','apartments':34,'scenario_funding_impact':[{'scenario_id':'S1','name':'GEBALANCEERD','funding_gap_eur':3400}]}
 x=assess_member_affordability_fairness(f,spread_years=1,affordability_limit_month_eur=10)
 assert x['scenario_affordability_fairness'][0]['average_monthly_extra_eur']<10

def test_fraction_allocation():
 f={'funding_id':'F1','scenario_funding_impact':[{'scenario_id':'S1','name':'A','funding_gap_eur':3000}]}
 members=[{'id':'A','breukdeel':1},{'id':'B','breukdeel':2}]
 x=assess_member_affordability_fairness(f,members,spread_years=1)
 a=x['scenario_affordability_fairness'][0]['allocations']
 assert a[1]['total_extra_contribution_eur']==2000

def test_no_automatic_changes():
 x=assess_member_affordability_fairness({'scenario_funding_impact':[]})
 assert x['automatic_contribution_change'] is False and x['automatic_decision'] is False
