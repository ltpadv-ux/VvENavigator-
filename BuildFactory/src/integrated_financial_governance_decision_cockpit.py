"""Enterprise 14.0 Integrated Financial Governance Decision Cockpit."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='14.0.0'

def _id(*parts:Any)->str:return 'GOVFIN-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()
def _num(v:Any)->float:
 try:return float(v or 0)
 except (TypeError,ValueError):return 0.0

def build_integrated_financial_governance_cockpit(optimizer:dict[str,Any], funding:dict[str,Any], fairness:dict[str,Any], smoothing:dict[str,Any], stress:dict[str,Any], governance:dict[str,Any]|None=None)->dict[str,Any]:
 governance=governance or {}
 scenarios={str(x.get('scenario_id')):x for x in optimizer.get('ranked_scenarios',[]) or []}
 funding_map={str(x.get('scenario_id')):x for x in funding.get('scenario_funding_impact',[]) or []}
 fairness_map={str(x.get('scenario_id')):x for x in fairness.get('scenario_affordability_fairness',[]) or []}
 stress_by_smoothing={str(x.get('smoothing_id')):x for x in stress.get('ranked_stress_paths',[]) or []}
 rows=[]
 for path in smoothing.get('ranked_funding_paths',[]) or []:
  sid=str(path.get('scenario_id','')); sc=scenarios.get(sid,{}); fi=funding_map.get(sid,{}); fa=fairness_map.get(sid,{}); st=stress_by_smoothing.get(str(path.get('smoothing_id','')),{})
  effect=_num(sc.get('effect_score',0)); feasibility=_num(sc.get('feasibility_score',0)); resilience=_num(fi.get('financial_resilience_score',0)); fair=_num(fa.get('fairness_score',0)); smooth=_num(path.get('smoothing_score',0)); stress_score=_num(st.get('stress_resilience_score',0)); mjop_ok=bool(path.get('mjop_buffer_ok',False)); reserve_ok=bool(path.get('reserve_floor_ok',False))
  governance_risk=_num(governance.get('governance_risk_score',0)); governance_score=max(0,100-governance_risk)
  integrated=round(effect*0.15+feasibility*0.10+resilience*0.15+fair*0.15+smooth*0.15+stress_score*0.20+governance_score*0.10,1)
  blocker=not (mjop_ok and reserve_ok) or st.get('stress_status')=='STRESS-ONVOLDOENDE'
  status='INTEGRAAL VOORKEURSPAD' if integrated>=80 and not blocker else ('INTEGRAAL AANDACHT' if integrated>=60 and not blocker else 'INTEGRAAL ONVOLDOENDE')
  rows.append({'decision_path_id':_id(path.get('smoothing_id',''),sid),'scenario_id':sid,'scenario_name':path.get('scenario_name'),'term_months':path.get('term_months'),'reserve_share_pct':path.get('reserve_share_pct'),'effect_score':effect,'feasibility_score':feasibility,'financial_resilience_score':resilience,'fairness_score':fair,'smoothing_score':smooth,'stress_resilience_score':stress_score,'governance_score':round(governance_score,1),'reserve_floor_ok':reserve_ok,'mjop_buffer_ok':mjop_ok,'maximum_monthly_extra_eur':path.get('maximum_monthly_extra_eur'),'stressed_max_monthly_extra_eur':st.get('stressed_max_monthly_extra_eur'),'reserve_after_eur':path.get('reserve_after_eur'),'stressed_reserve_after_eur':st.get('stressed_reserve_after_eur'),'mjop_space_after_eur':path.get('mjop_space_after_eur'),'integrated_decision_score':integrated,'decision_status':status,'blocker':blocker})
 rows.sort(key=lambda x:(x['blocker'],-x['integrated_decision_score'],_num(x.get('stressed_max_monthly_extra_eur',999999))))
 best=rows[0] if rows else None
 return {'integrated_financial_governance_decision_cockpit_version':ENGINE_VERSION,'cockpit_id':_id(optimizer.get('optimizer_id',''),stress.get('stress_test_id',''),len(rows)),'status':'INTEGRAAL BESLUITBEELD BESCHIKBAAR' if rows else 'ONVOLDOENDE INPUT VOOR INTEGRALE COCKPIT','decision_path_count':len(rows),'ranked_integrated_paths':rows,'integrated_preferred_path':best,'human_board_decision_required':bool(rows),'human_alv_approval_required':bool(rows),'human_legal_governance_review_required':bool(best and best.get('blocker')),'automatic_selection':False,'automatic_contribution_change':False,'automatic_reserve_draw':False,'automatic_financing':False,'automatic_decision':False,'automatic_execution':False,'next_action':'Leg het integrale voorkeursbeeld voor aan Bestuur/ALV met expliciete afweging van maandlast, fairness, reserve, MJOP en stressrisico.' if rows else 'Voer eerst scenario-, funding-, fairness-, smoothing- en stressanalyse uit.'}
