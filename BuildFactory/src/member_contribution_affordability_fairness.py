"""Enterprise 13.7 Member Contribution Affordability & Fairness Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='13.7.0'

def _id(*parts:Any)->str:return 'GOVAFF-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def assess_member_affordability_fairness(funding:dict[str,Any], members:list[dict[str,Any]]|None=None, spread_years:int=1, affordability_limit_month_eur:float=50.0)->dict[str,Any]:
 members=members or []
 if spread_years<1: spread_years=1
 rows=[]
 for s in funding.get('scenario_funding_impact',[]) or []:
  gap=_num(s.get('funding_gap_eur',0)); total_parts=sum(max(0,_num(m.get('fraction',m.get('breukdeel',0)))) for m in members)
  allocations=[]
  if members and total_parts>0:
   for m in members:
    part=max(0,_num(m.get('fraction',m.get('breukdeel',0))))/total_parts
    total=gap*part; monthly=total/(12*spread_years)
    burden_pct=None
    income=_num(m.get('monthly_disposable_income_eur',0))
    if income>0: burden_pct=round(monthly/income*100,2)
    affordable=monthly<=affordability_limit_month_eur if income<=0 else burden_pct<=5
    allocations.append({'member_id':m.get('member_id',m.get('id','')),'unit':m.get('unit',m.get('apartment','')),'fraction_share':round(part,6),'total_extra_contribution_eur':round(total,2),'monthly_extra_contribution_eur':round(monthly,2),'burden_pct_disposable_income':burden_pct,'affordable':affordable})
  else:
   apartments=max(1,int(_num(funding.get('apartments',34)))); total=gap/apartments; monthly=total/(12*spread_years)
   allocations=[{'member_id':'AVERAGE','unit':'Gemiddeld appartement','fraction_share':round(1/apartments,6),'total_extra_contribution_eur':round(total,2),'monthly_extra_contribution_eur':round(monthly,2),'burden_pct_disposable_income':None,'affordable':monthly<=affordability_limit_month_eur}]
  monthly_vals=[_num(a['monthly_extra_contribution_eur']) for a in allocations] or [0]
  unaffordable=sum(1 for a in allocations if not a['affordable'])
  max_month=max(monthly_vals); avg_month=sum(monthly_vals)/len(monthly_vals)
  current_share=max(0,min(1,_num(s.get('current_owner_benefit_share',0.5)))); future_share=round(1-current_share,2)
  intergen_score=round(100-abs(current_share-future_share)*100,1)
  affordability_score=round(max(0,100-(unaffordable/max(1,len(allocations))*70)-max(0,max_month-affordability_limit_month_eur)),1)
  fairness_score=round(affordability_score*0.6+intergen_score*0.4,1)
  status='BETAALBAAR & EVENWICHTIG' if fairness_score>=80 else ('AANDACHT' if fairness_score>=60 else 'HERIJKING BIJDRAGEPAD VEREIST')
  rows.append({'scenario_id':s.get('scenario_id'),'name':s.get('name'),'funding_gap_eur':gap,'spread_years':spread_years,'average_monthly_extra_eur':round(avg_month,2),'maximum_monthly_extra_eur':round(max_month,2),'unaffordable_member_count':unaffordable,'member_count':len(allocations),'affordability_score':affordability_score,'intergenerational_fairness_score':intergen_score,'fairness_score':fairness_score,'fairness_status':status,'current_owner_benefit_share':current_share,'future_owner_benefit_share':future_share,'allocations':allocations})
 rows.sort(key=lambda x:(x['fairness_status']!='BETAALBAAR & EVENWICHTIG',-x['fairness_score'],x['average_monthly_extra_eur']))
 return {'member_contribution_affordability_fairness_version':ENGINE_VERSION,'affordability_id':_id(funding.get('funding_id',''),spread_years,affordability_limit_month_eur),'status':'BETAALBAARHEID & FAIRNESS BEREKEND' if rows else 'GEEN FINANCIERINGSSCENARIOS BESCHIKBAAR','spread_years':spread_years,'affordability_limit_month_eur':affordability_limit_month_eur,'scenario_affordability_fairness':rows,'fairness_preferred_scenario':rows[0] if rows else None,'human_board_review_required':bool(rows),'human_alv_approval_required':bool(rows),'automatic_contribution_change':False,'automatic_allocation':False,'automatic_decision':False,'next_action':'Laat Bestuur/ALV betaalbaarheid, breukdelen, spreidingsduur en intergenerationele fairness gezamenlijk afwegen.' if rows else 'Voer eerst de Funding & Reserve Impact Engine uit.'}
