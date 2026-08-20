"""Enterprise 15.0 Adaptive VvE Financial Digital Twin."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='15.0.0'
HORIZONS=(1,5,10,30)

def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def _id(*parts:Any)->str:return 'GOVDTW-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()

def build_adaptive_financial_twin(actuals:dict[str,Any], mjop:dict[str,Any], finance:dict[str,Any], risk:dict[str,Any]|None=None, governance:dict[str,Any]|None=None, assumptions:dict[str,Any]|None=None)->dict[str,Any]:
 risk=risk or {}; governance=governance or {}; assumptions=assumptions or {}
 inflation=max(-0.05,_n(assumptions.get('inflation_rate',0.04))); reserve_yield=max(-0.05,_n(assumptions.get('reserve_yield_rate',0.02))); contribution_growth=max(-0.05,_n(assumptions.get('contribution_growth_rate',inflation)))
 reserve0=_n(finance.get('reserve_balance_eur')); cash0=_n(finance.get('cash_balance_eur')); annual_contrib=_n(finance.get('annual_contributions_eur')); annual_ops=_n(finance.get('annual_operating_cost_eur')); risk_cost=_n(risk.get('expected_annual_risk_cost_eur')); governance_penalty=max(0,min(1,_n(governance.get('governance_risk_score',0))/100))
 mjop_years={int(x.get('year',0)): _n(x.get('cost_eur')) for x in (mjop.get('annual_plan') or []) if int(x.get('year',0) or 0)>0}
 base_year=int(assumptions.get('base_year',1)); rows=[]; reserve=reserve0; cash=cash0; contribution=annual_contrib
 for year in range(1,max(HORIZONS)+1):
  contribution*=1+contribution_growth if year>1 else 1
  ops=annual_ops*((1+inflation)**(year-1)); planned=mjop_years.get(base_year+year-1,0); risk_adj=risk_cost*(1+governance_penalty); reserve=reserve*(1+reserve_yield)+contribution-ops-planned-risk_adj; cash=cash+max(0,contribution-ops)-min(max(cash,0),planned+risk_adj)
  rows.append({'year':year,'reserve_eur':round(reserve,2),'cash_eur':round(cash,2),'annual_contribution_eur':round(contribution,2),'operating_cost_eur':round(ops,2),'mjop_cost_eur':round(planned,2),'risk_cost_eur':round(risk_adj,2)})
 snapshots=[]
 for h in HORIZONS:
  r=rows[h-1]; stress=max(0,-r['reserve_eur'])+max(0,-r['cash_eur']); health=max(0,min(100,100-stress/1000-governance_penalty*20))
  snapshots.append({'horizon_years':h,**r,'financial_health_score':round(health,1),'status':'ROBUUST' if health>=80 else ('AANDACHT' if health>=60 else 'KRITIEK')})
 return {'adaptive_vve_financial_digital_twin_version':ENGINE_VERSION,'twin_id':_id(actuals.get('close_id',''),finance.get('forecast_id',''),reserve0,cash0),'status':'DIGITAL TWIN BESCHIKBAAR','horizons_years':list(HORIZONS),'snapshots':snapshots,'annual_projection':rows,'assumptions':{'inflation_rate':inflation,'reserve_yield_rate':reserve_yield,'contribution_growth_rate':contribution_growth,'governance_risk_score':round(governance_penalty*100,1)},'human_board_review_required':True,'automatic_contribution_change':False,'automatic_reserve_change':False,'automatic_mjop_change':False,'automatic_decision':False,'next_action':'Gebruik de 1/5/10/30-jaars snapshots voor scenariovergelijking, begroting, MJOP-herijking en ALV-besluitvorming.'}
