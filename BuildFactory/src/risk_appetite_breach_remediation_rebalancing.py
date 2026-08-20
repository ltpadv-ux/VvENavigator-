"""Enterprise 15.4 Risk Appetite Breach Remediation & Scenario Rebalancing Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='15.4.0'

def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def _id(*p:Any)->str:return 'GOVRBR-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()

def build_rebalancing_plan(ranking:dict[str,Any], finance:dict[str,Any]|None=None, rules:dict[str,Any]|None=None)->dict[str,Any]:
 finance=finance or {}; rules=rules or {}; rows=ranking.get('ranked_scenarios') or []; limits=ranking.get('appetite_limits_pct') or {}
 reserve_limit=_n(limits.get('reserve_shortfall',10)); liquidity_limit=_n(limits.get('liquidity_shortfall',10)); combined_limit=_n(limits.get('combined_shortfall',5)); apartments=max(1,int(_n(finance.get('apartments',34)) or 34)); reserve_balance=_n(finance.get('reserve_balance_eur')); annual_contrib=_n(finance.get('annual_contributions_eur'))
 if not rows:return {'risk_appetite_breach_remediation_rebalancing_version':ENGINE_VERSION,'status':'GEEN SCENARIORESULTATEN','automatic_rebalancing':False}
 target=next((x for x in rows if x.get('risk_appetite_status')=='BINNEN RISICOAPPETIJT'),rows[0]); rp=_n(target.get('reserve_shortfall_pct')); lp=_n(target.get('liquidity_shortfall_pct')); cp=_n(target.get('combined_shortfall_pct')); reserve_ex=max(0,rp-reserve_limit); liquidity_ex=max(0,lp-liquidity_limit); combined_ex=max(0,cp-combined_limit); severity=reserve_ex+liquidity_ex+combined_ex
 contribution_uplift_pct=min(25,round(severity*0.6,2)); extra_annual=round(annual_contrib*contribution_uplift_pct/100,2); extra_monthly_total=round(extra_annual/12,2); extra_monthly_per_apartment=round(extra_monthly_total/apartments,2)
 reserve_topup=round(max(0,reserve_balance*(min(30,severity*0.8)/100)),2); maintenance_deferral_pct=min(20,round(max(0,severity*0.4),2)); risk_reduction_target_pct=min(35,round(max(0,severity*0.7),2))
 actions=[]
 if contribution_uplift_pct>0:actions.append({'type':'CONTRIBUTION_UPLIFT','priority':1,'value_pct':contribution_uplift_pct,'annual_effect_eur':extra_annual,'monthly_per_apartment_eur':extra_monthly_per_apartment})
 if reserve_topup>0:actions.append({'type':'RESERVE_TOPUP','priority':2,'value_eur':reserve_topup})
 if maintenance_deferral_pct>0:actions.append({'type':'MJOP_REPHASING','priority':3,'value_pct':maintenance_deferral_pct,'guardrail':'Alleen niet-kritisch en technisch verantwoord onderhoud faseren.'})
 if risk_reduction_target_pct>0:actions.append({'type':'RISK_REDUCTION','priority':4,'value_pct':risk_reduction_target_pct,'guardrail':'Geen veiligheids-, compliance- of wettelijke risico’s uitstellen.'})
 projected_reserve=max(0,rp-contribution_uplift_pct*0.35-(reserve_topup/10000)); projected_liquidity=max(0,lp-contribution_uplift_pct*0.45-maintenance_deferral_pct*0.25); projected_combined=max(0,cp-contribution_uplift_pct*0.25-risk_reduction_target_pct*0.2); within=projected_reserve<=reserve_limit and projected_liquidity<=liquidity_limit and projected_combined<=combined_limit
 return {'risk_appetite_breach_remediation_rebalancing_version':ENGINE_VERSION,'rebalancing_id':_id(ranking.get('risk_appetite_id',''),target.get('scenario_name'),severity),'status':'HERBALANCERINGSPLAN BINNEN RISICOAPPETIJT GEPROJECTEERD' if within else 'AANVULLENDE HERIJKING NODIG','source_scenario':target.get('scenario_name'),'breach_severity_points':round(severity,2),'actions':actions,'projected_shortfall_pct':{'reserve':round(projected_reserve,2),'liquidity':round(projected_liquidity,2),'combined':round(projected_combined,2)},'projected_within_risk_appetite':within,'human_board_review_required':True,'human_alv_approval_required':True,'technical_mjop_review_required':True,'automatic_rebalancing':False,'automatic_contribution_change':False,'automatic_reserve_change':False,'automatic_mjop_change':False,'automatic_risk_appetite_change':False,'automatic_decision':False,'next_action':'Laat Bestuur/ALV het herbalanceringspakket beoordelen en voer daarna Monte Carlo opnieuw uit met geaccordeerde maatregelen.'}
