"""Enterprise 15.8 Scenario Activation, Baseline Freeze & Monitoring Covenant Engine."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='15.8.0'

def _n(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def _id(*p:Any)->str:return 'GOVACT-'+sha256('|'.join(str(x) for x in p).encode()).hexdigest()[:10].upper()

def activate_scenario_baseline(vote_validation:dict[str,Any], scenario:dict[str,Any], activation:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; mandate=vote_validation.get('activation_mandate') or {}; approved=bool(vote_validation.get('validated_for_manual_activation',False)); manual_confirmed=bool(activation.get('manual_activation_confirmed',False)); actor=str(activation.get('activated_by','')).strip(); activated_at=str(activation.get('activated_at','')).strip(); blockers=[]
 if not approved:blockers.append('Er is geen geldig ALV-activatiemandaat.')
 if not mandate:blockers.append('Activatiemandaat ontbreekt.')
 if not manual_confirmed:blockers.append('Handmatige activatiebevestiging ontbreekt.')
 if not actor:blockers.append('Activerende verantwoordelijke ontbreekt.')
 if not activated_at:blockers.append('Activatiemoment ontbreekt.')
 scenario_name=mandate.get('scenario_name') or scenario.get('scenario_name'); snaps=scenario.get('snapshots') or []; risk_limits=mandate.get('risk_appetite_limits_pct') or {}; verified=mandate.get('verified_shortfall_pct') or {}
 freeze={'scenario_name':scenario_name,'scenario_id':scenario.get('scenario_id'),'activation_mandate_id':mandate.get('mandate_id'),'activated_by':actor,'activated_at':activated_at,'activation_date':mandate.get('activation_date'),'execution_owner':mandate.get('execution_owner'),'risk_appetite_limits_pct':risk_limits,'verified_shortfall_pct':verified,'simulation_confidence_pct':mandate.get('simulation_confidence_pct'),'snapshots':snaps,'frozen':not blockers,'immutable_without_new_resolution':True}
 active=not blockers
 return {'scenario_activation_baseline_monitoring_covenant_version':ENGINE_VERSION,'activation_id':_id(mandate.get('mandate_id',''),scenario_name,activated_at),'status':'SCENARIO ACTIEF - BASELINE BEVROREN' if active else 'SCENARIO ACTIVATIE GEBLOKKEERD','blockers':blockers,'baseline_freeze':freeze if active else None,'monitoring_covenant':{'compare_actuals_to_baseline':True,'monitor_reserve':True,'monitor_liquidity':True,'monitor_contributions':True,'monitor_mjop':True,'monitor_risk_appetite':True,'monitor_confidence_drift':True,'material_variance_pct':_n(rules.get('material_variance_pct',5)),'breach_requires_board_review':True,'breach_requires_reforecast':True,'breach_requires_new_resolution_if_scope_changes':True} if active else None,'active':active,'human_activation_required':True,'automatic_activation':False,'automatic_baseline_change':False,'automatic_contribution_change':False,'automatic_reserve_change':False,'automatic_mjop_change':False,'automatic_decision':False,'next_action':'Start periodieke actual-vs-baseline monitoring en escaleer materiële afwijkingen volgens het monitoring covenant.' if active else 'Los activatieblokkades op voordat de scenario-baseline wordt bevroren.'}

def monitor_actuals_against_baseline(activation_record:dict[str,Any], actuals:dict[str,Any], rules:dict[str,Any]|None=None)->dict[str,Any]:
 rules=rules or {}; baseline=activation_record.get('baseline_freeze') or {}; covenant=activation_record.get('monitoring_covenant') or {}; threshold=_n(rules.get('material_variance_pct',covenant.get('material_variance_pct',5))); snaps=baseline.get('snapshots') or []; horizon=int(actuals.get('horizon_years',1) or 1); snap=next((x for x in snaps if int(x.get('horizon_years',0) or 0)==horizon),snaps[0] if snaps else {})
 fields={'reserve_eur':'reserve_eur','cash_eur':'cash_eur','annual_contribution_eur':'annual_contribution_eur','mjop_cost_eur':'mjop_cost_eur'}; variances={}; breaches=[]
 for label,key in fields.items():
  b=_n(snap.get(key)); a=_n(actuals.get(key)); pct=round(((a-b)/abs(b)*100),2) if b else (0.0 if a==0 else 100.0); variances[label]={'baseline':round(b,2),'actual':round(a,2),'variance_pct':pct};
  if abs(pct)>=threshold:breaches.append(f'{label} wijkt materieel af van baseline.')
 risk=actuals.get('shortfall_pct') or {}; limits=baseline.get('risk_appetite_limits_pct') or {}
 if _n(risk.get('reserve'))>_n(limits.get('reserve',999)):breaches.append('Reserve-shortfall overschrijdt bevroren risicogrens.')
 if _n(risk.get('liquidity'))>_n(limits.get('liquidity',999)):breaches.append('Liquiditeit-shortfall overschrijdt bevroren risicogrens.')
 if _n(risk.get('combined'))>_n(limits.get('combined',999)):breaches.append('Combined shortfall overschrijdt bevroren risicogrens.')
 return {'scenario_activation_baseline_monitoring_covenant_version':ENGINE_VERSION,'monitoring_status':'BASELINE BREACH - BESTUURLIJKE REVIEW VEREIST' if breaches else 'BASELINE OP KOERS','activation_id':activation_record.get('activation_id'),'horizon_years':horizon,'variances':variances,'breaches':breaches,'requires_board_review':bool(breaches),'requires_reforecast':bool(breaches),'automatic_baseline_change':False,'automatic_decision':False}
