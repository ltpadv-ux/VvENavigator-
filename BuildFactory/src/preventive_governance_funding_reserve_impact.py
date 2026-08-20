"""Enterprise 13.6 Preventive Governance Funding & Reserve Impact Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='13.6.0'

def _id(*parts:Any)->str:return 'GOVFND-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def assess_funding_reserve_impact(optimizer:dict[str,Any], finance:dict[str,Any], apartments:int=34)->dict[str,Any]:
 reserve=_num(finance.get('reserve_fund_eur',0)); liquidity=_num(finance.get('liquidity_eur',reserve)); mjop_space=_num(finance.get('mjop_available_space_eur',0)); min_reserve=_num(finance.get('minimum_reserve_eur',0)); annual_contrib=_num(finance.get('annual_contributions_eur',0))
 rows=[]
 for s in optimizer.get('ranked_scenarios',[]) or []:
  cost=_num(s.get('cost_eur',0)); after=max(0,reserve-cost); liquidity_after=max(0,liquidity-cost); reserve_floor_ok=after>=min_reserve; mjop_after=mjop_space-cost; gap=max(0,min_reserve-after)
  per_apartment=round(gap/max(1,apartments),2); monthly=round(per_apartment/12,2)
  resilience=round(max(0,min(100,(after/max(1,min_reserve))*70 + (liquidity_after/max(1,liquidity))*30)),1) if min_reserve>0 and liquidity>0 else (100.0 if cost<=reserve else 0.0)
  funding='RESERVE' if cost<=reserve and reserve_floor_ok else ('RESERVE + EXTRA BIJDRAGE' if cost<=reserve+annual_contrib else 'AANVULLENDE FINANCIERING VEREIST')
  status='FINANCIEEL ROBUUST' if reserve_floor_ok and mjop_after>=0 else ('AANDACHT' if reserve_floor_ok else 'ONVOLDOENDE RESERVEBUFFER')
  rows.append({'scenario_id':s.get('scenario_id'),'name':s.get('name'),'cost_eur':cost,'reserve_before_eur':reserve,'reserve_after_eur':round(after,2),'liquidity_after_eur':round(liquidity_after,2),'minimum_reserve_eur':min_reserve,'reserve_floor_ok':reserve_floor_ok,'mjop_space_after_eur':round(mjop_after,2),'funding_gap_eur':round(gap,2),'extra_contribution_per_apartment_eur':per_apartment,'extra_contribution_per_apartment_month_eur':monthly,'financial_resilience_score':resilience,'funding_route':funding,'funding_status':status,'optimization_score':s.get('optimization_score'),'threshold_shift_runs':s.get('threshold_shift_runs')})
 rows.sort(key=lambda x:(x['funding_status']!='FINANCIEEL ROBUUST',-x['financial_resilience_score'],-_num(x.get('optimization_score',0))))
 recommended=rows[0] if rows else None
 return {'preventive_governance_funding_reserve_impact_version':ENGINE_VERSION,'funding_id':_id(optimizer.get('optimizer_id',''),reserve,liquidity),'status':'FINANCIERINGSIMPACT BEREKEND' if rows else 'GEEN SCENARIOS VOOR FINANCIERINGSANALYSE','scenario_count':len(rows),'reserve_fund_eur':reserve,'liquidity_eur':liquidity,'mjop_available_space_eur':mjop_space,'minimum_reserve_eur':min_reserve,'apartments':apartments,'scenario_funding_impact':rows,'financially_preferred_scenario':recommended,'human_board_decision_required':bool(rows),'human_budget_approval_required':bool(rows),'automatic_funding':False,'automatic_contribution_change':False,'automatic_budget_commitment':False,'automatic_decision':False,'next_action':'Laat Bestuur/ALV effect, reserve-impact en eventuele extra bijdrage gezamenlijk afwegen.' if rows else 'Voer eerst scenario-optimalisatie uit.'}
