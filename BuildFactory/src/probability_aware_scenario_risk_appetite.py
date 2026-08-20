"""Enterprise 15.3 Probability-Aware Scenario Ranking & Risk Appetite Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='15.3.0'

def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def _id(*p:Any)->str:return 'GOVRAP-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()

def rank_probability_aware_scenarios(results:list[dict[str,Any]], appetite:dict[str,Any]|None=None)->dict[str,Any]:
 appetite=appetite or {}; reserve_limit=max(0,_n(appetite.get('max_reserve_shortfall_pct',10))); liquidity_limit=max(0,_n(appetite.get('max_liquidity_shortfall_pct',10))); combined_limit=max(0,_n(appetite.get('max_combined_shortfall_pct',5))); soft_penalty=_n(appetite.get('soft_limit_penalty_points',20)); hard_penalty=_n(appetite.get('hard_limit_penalty_points',50))
 ranked=[]
 for r in results:
  reserve_p=_n(r.get('probability_reserve_shortfall_pct')); liquidity_p=_n(r.get('probability_liquidity_shortfall_pct')); combined_p=_n(r.get('probability_combined_shortfall_pct')); p50_reserve=_n((r.get('ending_reserve_distribution_eur') or {}).get('p50')); p05_reserve=_n((r.get('ending_reserve_distribution_eur') or {}).get('p05')); p50_cash=_n((r.get('ending_cash_distribution_eur') or {}).get('p50')); deterministic=_n(r.get('deterministic_score',r.get('scenario_score',80)))
  breaches=[]
  if reserve_p>reserve_limit:breaches.append('RESERVE_SHORTFALL')
  if liquidity_p>liquidity_limit:breaches.append('LIQUIDITY_SHORTFALL')
  if combined_p>combined_limit:breaches.append('COMBINED_SHORTFALL')
  excess=max(0,reserve_p-reserve_limit)+max(0,liquidity_p-liquidity_limit)+max(0,combined_p-combined_limit)
  penalty=(hard_penalty if len(breaches)>=2 else soft_penalty if breaches else 0)+min(25,excess/2)
  downside_bonus=max(-10,min(10,p05_reserve/100000)); median_bonus=max(-10,min(10,(p50_reserve+p50_cash)/200000))
  score=round(max(0,min(100,deterministic-penalty+downside_bonus+median_bonus)),1)
  status='BINNEN RISICOAPPETIJT' if not breaches else ('BUITEN RISICOAPPETIJT' if len(breaches)==1 else 'NIET PASSEND BIJ RISICOAPPETIJT')
  ranked.append({'scenario_name':r.get('scenario_name'),'monte_carlo_id':r.get('monte_carlo_id'),'risk_appetite_status':status,'risk_appetite_score':score,'reserve_shortfall_pct':round(reserve_p,2),'liquidity_shortfall_pct':round(liquidity_p,2),'combined_shortfall_pct':round(combined_p,2),'breaches':breaches,'ending_reserve_p05_eur':round(p05_reserve,2),'ending_reserve_p50_eur':round(p50_reserve,2),'ending_cash_p50_eur':round(p50_cash,2)})
 ranked.sort(key=lambda x:(x['risk_appetite_status']!='BINNEN RISICOAPPETIJT',-x['risk_appetite_score']))
 preferred=ranked[0] if ranked else None
 return {'probability_aware_scenario_risk_appetite_version':ENGINE_VERSION,'risk_appetite_id':_id(reserve_limit,liquidity_limit,combined_limit,len(results)),'status':'RISICOAPPETIJT RANKING BESCHIKBAAR' if ranked else 'GEEN SCENARIORESULTATEN','appetite_limits_pct':{'reserve_shortfall':reserve_limit,'liquidity_shortfall':liquidity_limit,'combined_shortfall':combined_limit},'ranked_scenarios':ranked,'preferred_scenario':preferred,'human_board_review_required':True,'human_alv_approval_required':True,'automatic_scenario_selection':False,'automatic_risk_appetite_change':False,'automatic_contribution_change':False,'automatic_decision':False,'next_action':'Laat Bestuur/ALV de risicobereidheid expliciet vaststellen en beoordeel het voorkeurscenario inclusief downside-risico.'}
