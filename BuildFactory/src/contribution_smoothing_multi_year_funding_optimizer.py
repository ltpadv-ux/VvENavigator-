"""Enterprise 13.8 Contribution Smoothing & Multi-Year Funding Optimizer."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='13.8.0'

def _id(*parts:Any)->str:return 'GOVSMT-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def optimize_contribution_smoothing(funding:dict[str,Any], finance:dict[str,Any], members:list[dict[str,Any]]|None=None, terms_months:list[int]|None=None, reserve_shares:list[float]|None=None, affordability_limit_month_eur:float=50.0)->dict[str,Any]:
 members=members or []; terms_months=terms_months or [1,12,24,36,60]; reserve_shares=reserve_shares or [0.0,0.25,0.5,0.75]
 reserve=_num(finance.get('reserve_fund_eur',funding.get('reserve_fund_eur',0))); min_reserve=_num(finance.get('minimum_reserve_eur',funding.get('minimum_reserve_eur',0))); mjop_space=_num(finance.get('mjop_available_space_eur',funding.get('mjop_available_space_eur',0))); apartments=max(1,int(_num(funding.get('apartments',34))))
 total_parts=sum(max(0,_num(m.get('fraction',m.get('breukdeel',0)))) for m in members)
 rows=[]
 for scenario in funding.get('scenario_funding_impact',[]) or []:
  gap=max(0,_num(scenario.get('funding_gap_eur',0))); cost=max(0,_num(scenario.get('cost_eur',0)))
  for term in terms_months:
   term=max(1,int(term))
   for share in reserve_shares:
    share=max(0,min(1,_num(share))); reserve_draw=min(gap*share,max(0,reserve-min_reserve)); member_need=max(0,gap-reserve_draw)
    reserve_after=reserve-reserve_draw; mjop_after=mjop_space-reserve_draw
    if members and total_parts>0:
     monthlys=[]
     for m in members:
      part=max(0,_num(m.get('fraction',m.get('breukdeel',0))))/total_parts
      monthlys.append(member_need*part/term)
     max_month=max(monthlys) if monthlys else 0; avg_month=sum(monthlys)/len(monthlys) if monthlys else 0
    else:
     avg_month=member_need/apartments/term; max_month=avg_month
    affordability=max(0,min(100,100-max(0,max_month-affordability_limit_month_eur)*2))
    reserve_ok=reserve_after>=min_reserve; mjop_ok=mjop_after>=0
    smoothing=100 if max_month<=affordability_limit_month_eur else max(0,100-(max_month-affordability_limit_month_eur)*2)
    resilience=100 if reserve<=0 else max(0,min(100,reserve_after/max(1,reserve)*100))
    duration_penalty=min(20,term/3)
    score=round(smoothing*0.4+resilience*0.3+affordability*0.2+(100 if reserve_ok and mjop_ok else 0)*0.1-duration_penalty,1)
    status='ROBUST & BETAALBAAR' if reserve_ok and mjop_ok and max_month<=affordability_limit_month_eur else ('AANDACHT' if reserve_ok and mjop_ok else 'NIET PASSEND BINNEN BUFFER')
    rows.append({'smoothing_id':_id(scenario.get('scenario_id',''),term,share),'scenario_id':scenario.get('scenario_id'),'scenario_name':scenario.get('name'),'term_months':term,'reserve_share_pct':round(share*100,1),'reserve_draw_eur':round(reserve_draw,2),'member_funding_need_eur':round(member_need,2),'average_monthly_extra_eur':round(avg_month,2),'maximum_monthly_extra_eur':round(max_month,2),'reserve_after_eur':round(reserve_after,2),'mjop_space_after_eur':round(mjop_after,2),'reserve_floor_ok':reserve_ok,'mjop_buffer_ok':mjop_ok,'affordability_score':round(affordability,1),'smoothing_score':score,'funding_status':status,'estimated_years':round(term/12,2),'source_cost_eur':cost})
 rows.sort(key=lambda x:(x['funding_status']!='ROBUST & BETAALBAAR',-x['smoothing_score'],x['maximum_monthly_extra_eur'],x['term_months']))
 best=rows[0] if rows else None
 return {'contribution_smoothing_multi_year_funding_optimizer_version':ENGINE_VERSION,'optimizer_id':_id(funding.get('funding_id',''),len(rows)),'status':'SMOOTHING OPTIMALISATIE BEREKEND' if rows else 'GEEN FINANCIERINGSSCENARIOS BESCHIKBAAR','option_count':len(rows),'terms_months':terms_months,'reserve_shares':reserve_shares,'affordability_limit_month_eur':affordability_limit_month_eur,'ranked_funding_paths':rows,'recommended_funding_path':best,'human_board_review_required':bool(rows),'human_alv_approval_required':bool(rows),'automatic_contribution_change':False,'automatic_reserve_draw':False,'automatic_financing':False,'automatic_decision':False,'next_action':'Laat Bestuur/ALV het voorkeursbijdragepad beoordelen op maandlast, reservebuffer, MJOP-ruimte en spreidingsduur.' if rows else 'Voer eerst de Funding & Reserve Impact Engine uit.'}
