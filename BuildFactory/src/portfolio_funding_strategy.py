"""Compare financing mixes for portfolio funding gaps using reserve, contribution, loan, phasing and subsidy assumptions."""
from __future__ import annotations
from typing import Any

ENGINE_VERSION='7.3.0'

def _n(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _annuity(principal:float, annual_rate:float, years:int)->float:
    if principal<=0:return 0.0
    n=max(1,years*12); r=max(0.0,annual_rate)/12
    if r==0:return principal/n
    return principal*r/(1-(1+r)**(-n))

def build_portfolio_funding_strategy(allocation:dict[str,Any], assumptions:dict[str,Any]|None=None)->dict[str,Any]:
    assumptions=assumptions or {}; loan_rate=_n(assumptions.get('loan_rate',0.04)); loan_years=int(_n(assumptions.get('loan_years',15)) or 15); subsidy_rate=max(0,min(0.5,_n(assumptions.get('subsidy_rate',0.10)))); contribution_years=max(1,int(_n(assumptions.get('contribution_years',3)) or 3)); rows=[]
    for a in allocation.get('allocations',[]) or []:
        gap=max(0,_n(a.get('funding_gap'))); apartments=max(1,int(_n(a.get('apartments',34)) or 34))
        if gap<=0: continue
        scenarios=[]
        mixes=[('RESERVE + BIJDRAGE',0.40,0.60,0.0,0.0),('RESERVE + LENING',0.25,0.0,0.75,0.0),('SUBSIDIE + LENING',0.10,0.0,0.80,0.10),('FASEREN + MIX',0.20,0.30,0.40,0.10)]
        for name,reserve_share,contrib_share,loan_share,sub_share in mixes:
            subsidy=min(gap*sub_share,gap*subsidy_rate if subsidy_rate>0 else gap*sub_share); remaining=max(0,gap-subsidy); reserve=remaining*reserve_share/(reserve_share+contrib_share+loan_share) if reserve_share+contrib_share+loan_share else 0; contribution=remaining*contrib_share/(reserve_share+contrib_share+loan_share) if reserve_share+contrib_share+loan_share else 0; loan=max(0,remaining-reserve-contribution)
            monthly_loan=_annuity(loan,loan_rate,loan_years); monthly_contribution=contribution/(contribution_years*12); monthly_per_apartment=(monthly_loan+monthly_contribution)/apartments; interest_total=monthly_loan*loan_years*12-loan; total_30y=reserve+contribution+loan+max(0,interest_total); phasing_months=24 if name=='FASEREN + MIX' else 0
            affordability_score=max(0,100-monthly_per_apartment*2); leverage_score=max(0,100-(loan/gap*100)); subsidy_score=min(100,(subsidy/gap*100)*5 if gap else 0); speed_score=60 if phasing_months else 100; score=round(affordability_score*0.35+leverage_score*0.25+subsidy_score*0.20+speed_score*0.20,1)
            scenarios.append({'scenario':name,'reserve_use':round(reserve,2),'extra_contribution':round(contribution,2),'loan_amount':round(loan,2),'subsidy_amount':round(subsidy,2),'monthly_cost_total':round(monthly_loan+monthly_contribution,2),'monthly_cost_per_apartment':round(monthly_per_apartment,2),'loan_interest_total':round(max(0,interest_total),2),'phasing_months':phasing_months,'thirty_year_financing_cost':round(total_30y,2),'funding_score':score})
        scenarios=sorted(scenarios,key=lambda x:(-x['funding_score'],x['monthly_cost_per_apartment'],x['thirty_year_financing_cost']))
        for i,s in enumerate(scenarios,1): s['rank']=i
        rows.append({'name':a.get('name',''),'funding_gap':round(gap,2),'priority_score':a.get('priority_score',0),'scenarios':scenarios,'preferred_scenario':scenarios[0]['scenario'],'preferred_score':scenarios[0]['funding_score']})
    return {'portfolio_funding_strategy_version':ENGINE_VERSION,'status':'FINANCIERINGSSTRATEGIE BESCHIKBAAR' if rows else 'GEEN FINANCIERINGSGATEN','assumptions':{'loan_rate':loan_rate,'loan_years':loan_years,'subsidy_rate':subsidy_rate,'contribution_years':contribution_years},'vve_count':len(rows),'strategies':rows,'human_decision_required':bool(rows),'automatic_financing_commitment':False,'next_action':'Leg per VvE de voorkeursmix en alternatieven ter besluitvorming voor aan Bestuur/ALV.' if rows else 'Geen aanvullende financiering nodig.'}
