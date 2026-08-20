"""Enterprise 15.6 Confidence-Gated Board Recommendation & ALV Scenario Resolution Pack."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='15.6.0'

def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def _id(*p:Any)->str:return 'GOVSRP-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()

def build_confidence_gated_resolution_pack(confidence_gate:dict[str,Any], scenario:dict[str,Any], monte_carlo:dict[str,Any], finance:dict[str,Any]|None=None, context:dict[str,Any]|None=None)->dict[str,Any]:
 finance=finance or {}; context=context or {}
 if not confidence_gate.get('verified_for_board_decision',False):
  return {'confidence_gated_board_alv_scenario_resolution_pack_version':ENGINE_VERSION,'status':'BESLUITPAKKET GEBLOKKEERD DOOR CONFIDENCE GATE','gate_status':confidence_gate.get('status'),'blockers':confidence_gate.get('blockers',[]),'automatic_decision':False}
 name=scenario.get('scenario_name','GEVERIFIEERD SCENARIO'); snaps={int(x.get('horizon_years',0)):x for x in (scenario.get('snapshots') or [])}; limits=confidence_gate.get('risk_appetite_limits_pct') or {}; verified=confidence_gate.get('verified_shortfall_pct') or {}
 monthly_delta=_n(finance.get('extra_monthly_contribution_total_eur',finance.get('suggested_monthly_contribution_uplift_total_eur',0))); apartments=max(1,int(_n(finance.get('apartments',34)) or 34)); per_apartment=round(monthly_delta/apartments,2)
 impacts=[]
 for h in (5,10,30):
  s=snaps.get(h,{})
  impacts.append({'horizon_years':h,'reserve_eur':_n(s.get('reserve_eur')),'cash_eur':_n(s.get('cash_eur')),'financial_health_score':_n(s.get('financial_health_score')),'status':s.get('status')})
 recommendation='POSITIEF VOORLEGGEN AAN ALV'
 decision_points=['Vaststellen van het geverifieerde voorkeurscenario.','Bevestigen van de gehanteerde risicogrenzen en confidence gate.','Instemmen met de financiële maatregelen en eventuele bijdrage-impact.','Bestuur mandateren voor uitvoering binnen het vastgestelde scenario en bestaande governance-controls.']
 resolution=(f"De ALV besluit, onder voorbehoud van de toepasselijke statutaire en wettelijke vereisten, in te stemmen met scenario {name}. De vastgestelde risicogrenzen bedragen maximaal {limits.get('reserve','')}% kans op reservetekort, {limits.get('liquidity','')}% kans op liquiditeitstekort en {limits.get('combined','')}% gecombineerd tekort. De geverifieerde Monte Carlo-uitkomsten bedragen respectievelijk {verified.get('reserve','')}%, {verified.get('liquidity','')}% en {verified.get('combined','')}%, met een simulatie-confidence van {confidence_gate.get('simulation_confidence_pct','')}%. Het bestuur wordt gemandateerd de uitvoering binnen het goedgekeurde scenario, budget en governance-kaders voor te bereiden en te monitoren.")
 return {'confidence_gated_board_alv_scenario_resolution_pack_version':ENGINE_VERSION,'scenario_resolution_pack_id':_id(confidence_gate.get('confidence_gate_id',''),name,monte_carlo.get('monte_carlo_id','')),'status':'CONFIDENCE-GATED BESLUITPAKKET GEREED VOOR BESTUURLIJKE REVIEW','recommendation':recommendation,'scenario_name':name,'confidence_gate_status':confidence_gate.get('status'),'simulation_confidence_pct':confidence_gate.get('simulation_confidence_pct'),'risk_appetite_limits_pct':limits,'verified_shortfall_pct':verified,'monte_carlo_evidence':{'monte_carlo_id':monte_carlo.get('monte_carlo_id'),'simulations':monte_carlo.get('simulations'),'reserve_distribution_eur':monte_carlo.get('ending_reserve_distribution_eur'),'cash_distribution_eur':monte_carlo.get('ending_cash_distribution_eur')},'horizon_impacts':impacts,'financial_effect':{'extra_monthly_contribution_total_eur':round(monthly_delta,2),'extra_monthly_contribution_per_apartment_eur':per_apartment},'decision_points':decision_points,'board_narrative':{'subject':context.get('subject','Confidence-gated scenario besluit'),'rationale':'Scenario is opnieuw probabilistisch geverifieerd en voldoet aan de vastgestelde risicogrenzen en confidence floor.'},'draft_alv_resolution':resolution,'human_board_review_required':True,'human_alv_approval_required':True,'human_legal_governance_review_required':True,'automatic_resolution_adoption':False,'automatic_scenario_activation':False,'automatic_contribution_change':False,'automatic_reserve_change':False,'automatic_mjop_change':False,'automatic_decision':False,'automatic_execution':False,'next_action':'Laat Bestuur het besluitpakket controleren en leg daarna de definitieve besluittekst, Monte Carlo-bewijs en 5/10/30-jaars gevolgen voor aan de ALV.'}
