"""Enterprise 13.9 Contribution Path Stress Test & Payment Shock Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='13.9.0'

def _id(*parts:Any)->str:return 'GOVSHK-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def stress_test_contribution_paths(smoothing:dict[str,Any], shocks:dict[str,Any]|None=None)->dict[str,Any]:
 shocks=shocks or {}
 inflation=max(0,_num(shocks.get('inflation_pct',4)))/100
 mjop_shock=max(0,_num(shocks.get('unexpected_mjop_cost_eur',0)))
 energy_shock=max(0,_num(shocks.get('annual_energy_cost_increase_eur',0)))
 interest=max(0,_num(shocks.get('interest_rate_pct',4)))/100
 arrears=max(0,min(1,_num(shocks.get('contribution_arrears_pct',0))/100))
 reserve_build_reduction=max(0,min(1,_num(shocks.get('reserve_build_reduction_pct',0))/100))
 rows=[]
 for p in smoothing.get('ranked_funding_paths',[]) or []:
  term=max(1,int(_num(p.get('term_months',1))))
  base_month=_num(p.get('maximum_monthly_extra_eur',0)); reserve_after=_num(p.get('reserve_after_eur',0)); mjop_after=_num(p.get('mjop_space_after_eur',0)); member_need=_num(p.get('member_funding_need_eur',0))
  inflated_month=base_month*(1+inflation)
  financing_interest=(member_need*interest*(term/12))/max(1,term)
  payment_shock=inflated_month+financing_interest
  arrears_effect=payment_shock*arrears
  net_payment_shock=payment_shock+arrears_effect
  reserve_loss=mjop_shock + energy_shock*(term/12) + reserve_after*reserve_build_reduction
  stressed_reserve=reserve_after-reserve_loss
  stressed_mjop=mjop_after-mjop_shock
  buffer_fail=stressed_reserve<0 or stressed_mjop<0
  payment_score=max(0,100-net_payment_shock*1.5)
  buffer_score=max(0,min(100,100 if not buffer_fail else 40 + min(0,stressed_reserve)/1000))
  resilience=round(max(0,min(100,payment_score*0.45+buffer_score*0.40+(100 if not buffer_fail else 0)*0.15)),1)
  status='STRESS-ROBUUST' if resilience>=80 and not buffer_fail else ('STRESS-AANDACHT' if resilience>=60 else 'STRESS-ONVOLDOENDE')
  rows.append({'stress_id':_id(p.get('smoothing_id',''),inflation,mjop_shock,arrears),'smoothing_id':p.get('smoothing_id'),'scenario_name':p.get('scenario_name'),'term_months':term,'reserve_share_pct':p.get('reserve_share_pct'),'base_max_monthly_extra_eur':round(base_month,2),'stressed_max_monthly_extra_eur':round(net_payment_shock,2),'stressed_reserve_after_eur':round(stressed_reserve,2),'stressed_mjop_space_after_eur':round(stressed_mjop,2),'buffer_failure':buffer_fail,'stress_resilience_score':resilience,'stress_status':status})
 rows.sort(key=lambda x:(x['stress_status']!='STRESS-ROBUUST',-x['stress_resilience_score'],x['stressed_max_monthly_extra_eur']))
 return {'contribution_path_stress_test_payment_shock_version':ENGINE_VERSION,'stress_test_id':_id(smoothing.get('optimizer_id',''),len(rows)),'status':'STRESS TEST BEREKEND' if rows else 'GEEN BIJDRAGEPADEN BESCHIKBAAR','shock_assumptions':{'inflation_pct':inflation*100,'unexpected_mjop_cost_eur':mjop_shock,'annual_energy_cost_increase_eur':energy_shock,'interest_rate_pct':interest*100,'contribution_arrears_pct':arrears*100,'reserve_build_reduction_pct':reserve_build_reduction*100},'ranked_stress_paths':rows,'stress_preferred_path':rows[0] if rows else None,'human_board_review_required':bool(rows),'human_alv_approval_required':bool(rows),'automatic_contribution_change':False,'automatic_financing':False,'automatic_decision':False,'next_action':'Laat Bestuur/ALV het stress-robuuste bijdragepad afwegen tegen maandlast, reservebuffer en MJOP-risico.' if rows else 'Voer eerst de Contribution Smoothing Optimizer uit.'}
