"""Enterprise 15.1 Digital Twin Scenario Branching & What-If Simulation."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
from .adaptive_vve_financial_digital_twin import build_adaptive_financial_twin
ENGINE_VERSION='15.1.0'
DEFAULT_SCENARIOS=(
 {'scenario_id':'BASIS','name':'Basis','assumptions':{}},
 {'scenario_id':'VERSNELD_ONDERHOUD','name':'Versneld onderhoud','assumptions':{'mjop_multiplier':1.20}},
 {'scenario_id':'VERDUURZAMING','name':'Verduurzaming','assumptions':{'mjop_multiplier':1.10,'operating_cost_multiplier':0.90,'risk_cost_multiplier':0.90}},
 {'scenario_id':'HOGERE_INFLATIE','name':'Hogere inflatie','assumptions':{'inflation_rate':0.06}},
 {'scenario_id':'LAGERE_RESERVE_OPBOUW','name':'Lagere reserve-opbouw','assumptions':{'contribution_growth_rate':0.01,'reserve_yield_rate':0.01}},
 {'scenario_id':'BIJDRAGE_VERHOGING','name':'Bijdrageverhoging','assumptions':{'annual_contribution_multiplier':1.10,'contribution_growth_rate':0.04}},
)
def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0
def _id(*p:Any)->str:return 'GOVSCN-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()
def _scaled_mjop(mjop:dict[str,Any], mult:float)->dict[str,Any]:
 return {**mjop,'annual_plan':[{**x,'cost_eur':round(_n(x.get('cost_eur'))*mult,2)} for x in (mjop.get('annual_plan') or [])]}
def simulate_digital_twin_scenarios(actuals:dict[str,Any], mjop:dict[str,Any], finance:dict[str,Any], risk:dict[str,Any]|None=None, governance:dict[str,Any]|None=None, base_assumptions:dict[str,Any]|None=None, scenarios:list[dict[str,Any]]|None=None)->dict[str,Any]:
 risk=risk or {}; governance=governance or {}; base_assumptions=base_assumptions or {}; scenarios=scenarios or [dict(x) for x in DEFAULT_SCENARIOS]; rows=[]
 for s in scenarios:
  a={**base_assumptions,**(s.get('assumptions') or {})}; mm=max(0,_n(a.pop('mjop_multiplier',1)) or 1); om=max(0,_n(a.pop('operating_cost_multiplier',1)) or 1); rm=max(0,_n(a.pop('risk_cost_multiplier',1)) or 1); cm=max(0,_n(a.pop('annual_contribution_multiplier',1)) or 1)
  f={**finance,'annual_operating_cost_eur':_n(finance.get('annual_operating_cost_eur'))*om,'annual_contributions_eur':_n(finance.get('annual_contributions_eur'))*cm}; r={**risk,'expected_annual_risk_cost_eur':_n(risk.get('expected_annual_risk_cost_eur'))*rm}; m=_scaled_mjop(mjop,mm)
  twin=build_adaptive_financial_twin(actuals,m,f,r,governance,a); snaps={x['horizon_years']:x for x in twin.get('snapshots',[])}; s5=snaps.get(5,{}); s10=snaps.get(10,{}); s30=snaps.get(30,{})
  score=round(_n(s5.get('financial_health_score'))*0.25+_n(s10.get('financial_health_score'))*0.35+_n(s30.get('financial_health_score'))*0.40,1); min_res=min((_n(x.get('reserve_eur')) for x in twin.get('annual_projection',[])),default=0); min_cash=min((_n(x.get('cash_eur')) for x in twin.get('annual_projection',[])),default=0); critical=sum(1 for x in twin.get('snapshots',[]) if x.get('status')=='KRITIEK')
  rows.append({'scenario_id':s.get('scenario_id'),'scenario_name':s.get('name'),'scenario_score':score,'critical_snapshot_count':critical,'minimum_reserve_eur':round(min_res,2),'minimum_cash_eur':round(min_cash,2),'snapshot_1y':snaps.get(1),'snapshot_5y':s5,'snapshot_10y':s10,'snapshot_30y':s30,'assumptions':s.get('assumptions') or {},'twin_id':twin.get('twin_id')})
 rows.sort(key=lambda x:(x['critical_snapshot_count'],-x['scenario_score'],-x['minimum_reserve_eur'],-x['minimum_cash_eur'])); best=rows[0] if rows else None
 return {'digital_twin_scenario_branching_what_if_version':ENGINE_VERSION,'simulation_id':_id(actuals.get('close_id',''),len(rows),best.get('scenario_id') if best else ''),'status':'SCENARIOVERGELIJKING BESCHIKBAAR' if rows else 'GEEN SCENARIO’S BESCHIKBAAR','scenario_count':len(rows),'ranked_scenarios':rows,'preferred_scenario':best,'ranking_logic':'25% health 5 jaar + 35% health 10 jaar + 40% health 30 jaar, met KRITIEK-status als primaire straf.','human_board_review_required':True,'human_alv_approval_required':True,'automatic_scenario_selection':False,'automatic_contribution_change':False,'automatic_mjop_change':False,'automatic_decision':False,'next_action':'Vergelijk de scenario’s op 5/10/30 jaar en leg het voorkeurscenario met aannames en risico’s voor aan Bestuur/ALV.'}
