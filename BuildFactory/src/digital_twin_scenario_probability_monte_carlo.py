"""Enterprise 15.2 Digital Twin Scenario Probability & Monte Carlo Risk Engine."""
from __future__ import annotations
import random
from hashlib import sha256
from typing import Any
ENGINE_VERSION='15.2.0'

def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def _id(*p:Any)->str:return 'GOVMCR-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()

def run_scenario_monte_carlo(scenario:dict[str,Any], simulations:int=2000, seed:int=42, rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; simulations=max(100,int(simulations)); rng=random.Random(seed)
 snap=(scenario.get('snapshots') or [{}])[-1]; years=int(snap.get('horizon_years',30) or 30)
 reserve0=_n(rules.get('start_reserve_eur',scenario.get('start_reserve_eur',snap.get('reserve_eur',0)))); cash0=_n(rules.get('start_cash_eur',scenario.get('start_cash_eur',snap.get('cash_eur',0)))); annual_contrib=_n(rules.get('annual_contributions_eur',scenario.get('annual_contributions_eur',snap.get('annual_contribution_eur',0)))); annual_ops=_n(rules.get('annual_operating_cost_eur',scenario.get('annual_operating_cost_eur',snap.get('operating_cost_eur',0)))); annual_mjop=max(0,_n(rules.get('annual_mjop_cost_eur',scenario.get('annual_mjop_cost_eur',snap.get('mjop_cost_eur',0))))); annual_risk=max(0,_n(rules.get('annual_risk_cost_eur',scenario.get('annual_risk_cost_eur',snap.get('risk_cost_eur',0)))))
 inflation_mu=_n(rules.get('inflation_mean',0.04)); inflation_sd=max(0,_n(rules.get('inflation_sd',0.015))); maintenance_sd=max(0,_n(rules.get('maintenance_cost_sd_pct',0.15))); contribution_sd=max(0,_n(rules.get('contribution_growth_sd_pct',0.01))); shock_prob=min(1,max(0,_n(rules.get('annual_adverse_shock_probability',0.08)))); shock_cost=max(0,_n(rules.get('adverse_shock_cost_eur',25000)))
 reserve_fail=0; liquidity_fail=0; both_fail=0; end_reserves=[]; end_cash=[]
 for _ in range(simulations):
  reserve=reserve0; cash=cash0; contribution=annual_contrib
  had_reserve_fail=False; had_cash_fail=False
  for y in range(1,years+1):
   inflation=max(-0.03,rng.gauss(inflation_mu,inflation_sd)); contribution*=1+max(-0.05,rng.gauss(inflation_mu,contribution_sd)) if y>1 else 1
   ops=annual_ops*((1+inflation)**(y-1)); mjop=annual_mjop*max(0.25,rng.gauss(1,maintenance_sd)); risk=annual_risk
   shock=shock_cost if rng.random()<shock_prob else 0
   out=ops+mjop+risk+shock; reserve+=contribution-out; cash+=max(0,contribution-ops)-min(max(cash,0),mjop+risk+shock)
   had_reserve_fail=had_reserve_fail or reserve<0; had_cash_fail=had_cash_fail or cash<0
  reserve_fail+=int(had_reserve_fail); liquidity_fail+=int(had_cash_fail); both_fail+=int(had_reserve_fail and had_cash_fail); end_reserves.append(reserve); end_cash.append(cash)
 end_reserves.sort(); end_cash.sort()
 def pct(xs:list[float],q:float)->float:
  i=min(len(xs)-1,max(0,int(round((len(xs)-1)*q)))); return round(xs[i],2)
 reserve_p=round(reserve_fail/simulations*100,2); liquidity_p=round(liquidity_fail/simulations*100,2); both_p=round(both_fail/simulations*100,2); risk=max(reserve_p,liquidity_p)
 status='LAAG RISICO' if risk<10 else ('MATIG RISICO' if risk<25 else ('HOOG RISICO' if risk<50 else 'KRITIEK RISICO'))
 return {'digital_twin_scenario_probability_monte_carlo_version':ENGINE_VERSION,'monte_carlo_id':_id(scenario.get('scenario_id',''),simulations,seed,years),'scenario_name':scenario.get('scenario_name'),'simulations':simulations,'horizon_years':years,'status':status,'probability_reserve_shortfall_pct':reserve_p,'probability_liquidity_shortfall_pct':liquidity_p,'probability_combined_shortfall_pct':both_p,'ending_reserve_distribution_eur':{'p05':pct(end_reserves,.05),'p50':pct(end_reserves,.50),'p95':pct(end_reserves,.95)},'ending_cash_distribution_eur':{'p05':pct(end_cash,.05),'p50':pct(end_cash,.50),'p95':pct(end_cash,.95)},'risk_drivers':{'inflation_mean':inflation_mu,'inflation_sd':inflation_sd,'maintenance_cost_sd_pct':maintenance_sd,'annual_adverse_shock_probability':shock_prob,'adverse_shock_cost_eur':shock_cost},'human_board_review_required':True,'automatic_scenario_selection':False,'automatic_contribution_change':False,'automatic_reserve_change':False,'automatic_mjop_change':False,'automatic_decision':False,'next_action':'Gebruik kansverdelingen naast deterministic scenario ranking; herijk aannames wanneer shortfall-kansen boven bestuurlijke risicotolerantie komen.'}
