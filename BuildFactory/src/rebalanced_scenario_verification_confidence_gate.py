"""Enterprise 15.5 Rebalanced Scenario Verification & Confidence Gate."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='15.5.0'

def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def _id(*p:Any)->str:return 'GOVCFG-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()

def verify_rebalanced_scenario(rebalancing:dict[str,Any], monte_carlo:dict[str,Any], appetite:dict[str,Any]|None=None, rules:dict[str,Any]|None=None)->dict[str,Any]:
 appetite=appetite or {}; rules=rules or {}
 reserve_limit=_n(appetite.get('max_reserve_shortfall_pct',10)); liquidity_limit=_n(appetite.get('max_liquidity_shortfall_pct',10)); combined_limit=_n(appetite.get('max_combined_shortfall_pct',5)); confidence_floor=_n(rules.get('minimum_confidence_pct',95))
 reserve_p=_n(monte_carlo.get('probability_reserve_shortfall_pct')); liquidity_p=_n(monte_carlo.get('probability_liquidity_shortfall_pct')); combined_p=_n(monte_carlo.get('probability_combined_shortfall_pct'))
 reserve_ok=reserve_p<=reserve_limit; liquidity_ok=liquidity_p<=liquidity_limit; combined_ok=combined_p<=combined_limit
 sims=max(0,int(_n(monte_carlo.get('simulations')))); confidence=min(99.9,max(0,100-(100/(max(sims,1)**0.5)))) if sims else 0
 projection_consistent=bool(rebalancing.get('projected_within_risk_appetite',False)) == bool(reserve_ok and liquidity_ok and combined_ok)
 blockers=[]
 if not reserve_ok:blockers.append('Reserve shortfall probability ligt boven de vastgestelde risicogrens.')
 if not liquidity_ok:blockers.append('Liquidity shortfall probability ligt boven de vastgestelde risicogrens.')
 if not combined_ok:blockers.append('Combined shortfall probability ligt boven de vastgestelde risicogrens.')
 if confidence<confidence_floor:blockers.append('Simulatievertrouwen ligt onder de vereiste confidence floor.')
 if not projection_consistent:blockers.append('Herbalanceringsprojectie en nieuwe Monte Carlo-uitkomst zijn niet consistent.')
 passed=not blockers
 return {'rebalanced_scenario_verification_confidence_gate_version':ENGINE_VERSION,'confidence_gate_id':_id(rebalancing.get('rebalancing_id',''),monte_carlo.get('monte_carlo_id',''),reserve_p,liquidity_p,combined_p),'status':'CONFIDENCE GATE GESLAAGD' if passed else 'CONFIDENCE GATE GEBLOKKEERD','risk_appetite_limits_pct':{'reserve':reserve_limit,'liquidity':liquidity_limit,'combined':combined_limit},'verified_shortfall_pct':{'reserve':round(reserve_p,2),'liquidity':round(liquidity_p,2),'combined':round(combined_p,2)},'reserve_within_limit':reserve_ok,'liquidity_within_limit':liquidity_ok,'combined_within_limit':combined_ok,'simulation_confidence_pct':round(confidence,2),'minimum_confidence_pct':confidence_floor,'projection_consistent':projection_consistent,'blockers':blockers,'verified_for_board_decision':passed,'human_board_review_required':True,'human_alv_approval_required':True,'automatic_scenario_activation':False,'automatic_contribution_change':False,'automatic_reserve_change':False,'automatic_mjop_change':False,'automatic_decision':False,'next_action':'Leg het geverifieerde scenario ter besluitvorming voor aan Bestuur/ALV.' if passed else 'Herijk het herstelpakket en voer een nieuwe Monte Carlo-verificatie uit.'}
