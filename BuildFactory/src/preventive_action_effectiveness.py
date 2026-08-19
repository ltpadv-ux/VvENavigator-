"""Enterprise 10.6 Preventive Action Effectiveness & Avoided Cost Verification."""
from __future__ import annotations
from typing import Any
ENGINE_VERSION='10.6.0'

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def verify_preventive_action_effectiveness(mandate_result:dict[str,Any], actuals:dict[str,Any], baseline:dict[str,Any]|None=None)->dict[str,Any]:
    baseline=baseline or {}
    mandate=mandate_result.get('mandate',{}) or {}
    if mandate_result.get('status')!='VROEG-ACTIEMANDAAT ACTIEF' or not mandate:
        return {'preventive_action_effectiveness_version':ENGINE_VERSION,'status':'GEEN ACTIEF PREVENTIEF MANDAAT','verification':{},'automatic_closure':False}
    target_health=_num(mandate.get('target_health_score')); target_risk=_num(mandate.get('target_risk_score'))
    actual_health=_num(actuals.get('health_governance_score')); actual_risk=_num(actuals.get('risk_score'))
    progress=_num(actuals.get('progress_pct',mandate.get('progress_pct',0))); evidence=actuals.get('evidence',mandate.get('evidence',[])) or []
    planned_cost=_num(mandate.get('budget')); actual_spend=_num(actuals.get('actual_spend',mandate.get('actual_spend',0)))
    expected_avoided=_num(mandate.get('expected_avoided_recovery_cost'))
    counterfactual_cost=_num(actuals.get('counterfactual_recovery_cost',baseline.get('counterfactual_recovery_cost',planned_cost+expected_avoided)))
    verified_avoided=max(0.0,round(counterfactual_cost-actual_spend,2))
    baseline_health=_num(baseline.get('health_governance_score',actuals.get('baseline_health_governance_score',0)))
    baseline_risk=_num(baseline.get('risk_score',actuals.get('baseline_risk_score',100)))
    health_uplift=round(actual_health-baseline_health,1) if baseline_health else 0.0
    risk_reduction=round(baseline_risk-actual_risk,1) if baseline_risk else 0.0
    health_ok=actual_health>=target_health
    risk_ok=actual_risk<=target_risk
    execution_ok=progress>=100 and bool(evidence)
    cost_ok=actual_spend<=planned_cost
    avoided_ok=verified_avoided>=expected_avoided*0.8 if expected_avoided>0 else True
    trend_turned=bool(actuals.get('trend_turned',health_uplift>0 and risk_reduction>0))
    checks={'health_target_met':health_ok,'risk_target_met':risk_ok,'execution_complete':execution_ok,'within_budget':cost_ok,'avoided_cost_verified':avoided_ok,'trend_turned':trend_turned}
    passed=sum(1 for v in checks.values() if v); score=round(passed/len(checks)*100,1)
    effective=all(checks.values())
    status='PREVENTIEF EFFECT BEWEZEN' if effective else ('DEELS EFFECTIEF' if score>=66.7 else 'NADER HERSTEL NODIG')
    return {'preventive_action_effectiveness_version':ENGINE_VERSION,'status':status,'effectiveness_score':score,'checks':checks,'verification':{'target_health_score':target_health,'actual_health_score':actual_health,'health_uplift_vs_baseline':health_uplift,'target_risk_score':target_risk,'actual_risk_score':actual_risk,'risk_reduction_vs_baseline':risk_reduction,'planned_cost':planned_cost,'actual_spend':actual_spend,'expected_avoided_recovery_cost':expected_avoided,'verified_avoided_recovery_cost':verified_avoided,'avoidance_realization_pct':round((verified_avoided/expected_avoided*100),1) if expected_avoided>0 else 100.0},'human_closure_required':True,'automatic_closure':False,'next_action':'Laat Bestuur/ALV het preventieve effect en de vermeden kosten formeel bevestigen.' if effective else 'Beoordeel tekortschietende checks en stuur de preventieve maatregel bij.'}
