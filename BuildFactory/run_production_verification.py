#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/"src"))
from production_orchestrator import run_production_release
from production_verification import verify_production_result
from verification_diagnostics import diagnose_verification
from self_healing import run_self_healing
from release_control_center import build_release_control_center
from release_history import append_history
from reliability_sla import evaluate_reliability_sla
from sla_improvement_engine import analyze_sla_root_causes
from improvement_backlog import update_backlog_file
from improvement_governance import govern_improvement_closure
from autonomous_governance import build_governance_cycle
from governance_decision_register import build_decision_register
from alv_decision_workflow import build_alv_workflow
from alv_mandate_control import build_execution_mandates
from mandate_compliance import evaluate_mandate_compliance
from mandate_forecast import forecast_mandates
from corrective_action_optimizer import optimize_corrective_actions
from corrective_decision_workflow import build_corrective_decisions, approved_mandate_amendments
from mandate_amendment_engine import apply_mandate_amendments
from amendment_effectiveness import evaluate_amendment_effectiveness
from governance_control_tower import build_control_tower
from executive_risk_radar import build_risk_radar
from strategic_scenario_radar import build_strategic_scenario_radar
from scenario_strategy_lock import build_strategy_lock
from strategy_execution_scorecard import build_strategy_execution_scorecard
from strategy_intervention_engine import build_strategy_interventions
from intervention_impact_simulator import simulate_intervention_impacts
from intervention_decision_matrix import build_intervention_decision_matrix
from intervention_execution_mandate import build_intervention_execution_mandate
from execution_benefits_tracking import track_execution_and_benefits
from closed_loop_management import build_closed_loop_management

def main()->int:
 p=argparse.ArgumentParser(description="VvE Navigator 7.0 Closed-Loop VvE Management Platform"); p.add_argument("dataset",nargs="?",default=str(ROOT/"data"/"sample_vve_34.json")); p.add_argument("--output",default=str(ROOT/"artifacts"/"verification")); p.add_argument("--horizon",type=int,default=30); p.add_argument("--self-heal",action="store_true",default=True); p.add_argument("--sla",type=float,default=95.0); p.add_argument("--closure-runs",type=int,default=3); p.add_argument("--mandate-warning-days",type=int,default=30); p.add_argument("--risk-outlook-months",type=int,default=12); p.add_argument("--discount-rate",type=float,default=0.03); a=p.parse_args()
 release=run_production_release(a.dataset,a.output,horizon_years=a.horizon); verification=verify_production_result(release); diagnostics=diagnose_verification(verification,release); healing=run_self_healing(release,max_attempts=1) if a.self_heal and not verification.get("verified") else {"status":"NOT_NEEDED","after":verification,"escalation_required":False,"repairs":[],"human_actions":[]}; final_verification=healing.get("after",verification); final_diagnostics=diagnose_verification(final_verification,release); report={"release":release,"verification":final_verification,"diagnostics":final_diagnostics,"self_healing":healing}; control=build_release_control_center(report); report["control_center"]=control
 out=Path(a.output); out.mkdir(parents=True,exist_ok=True); history_path=out/"release-history.json"; trend=append_history(history_path,report); sla=evaluate_reliability_sla(trend,minimum_reliability=a.sla,max_blocked_recent=1)
 try: history=json.loads(history_path.read_text(encoding="utf-8"))
 except Exception: history=[]
 improvement=analyze_sla_root_causes(history,[final_diagnostics]); backlog_path=out/"continuous-improvement-backlog.json"; backlog=update_backlog_file(backlog_path,improvement); governance=govern_improvement_closure(backlog,history,sla,improvement,required_stable_runs=a.closure_runs); governed_backlog={**backlog,"items":governance["items"],"open_count":governance["open_count"],"status":"BIJGEWERKT" if governance["open_count"]==0 else "ACTIE VEREIST","next_action":governance["next_action"]}; backlog_path.write_text(json.dumps(governed_backlog,ensure_ascii=False,indent=2),encoding="utf-8")
 report.update(trend_monitor=trend,reliability_sla=sla,sla_improvement=improvement,improvement_backlog=governed_backlog,improvement_governance=governance); autonomous=build_governance_cycle(report); report["autonomous_governance"]=autonomous
 register_path=out/"governance-decision-register.json"
 try: existing_register=json.loads(register_path.read_text(encoding="utf-8"))
 except Exception: existing_register={}
 register=build_decision_register(autonomous,existing_register); register_path.write_text(json.dumps(register,ensure_ascii=False,indent=2),encoding="utf-8"); report["governance_decision_register"]=register
 alv_path=out/"alv-decision-workflow.json"
 try: existing_alv=json.loads(alv_path.read_text(encoding="utf-8"))
 except Exception: existing_alv={}
 metrics=((release.get("executive_cockpit",{}) or {}).get("key_metrics",{}) or {}); alv=build_alv_workflow(register,{"monthly_per_apartment":metrics.get("monthly_per_apartment",0.0),"reserve_impact":metrics.get("reserve",0.0)},existing_alv); alv_path.write_text(json.dumps(alv,ensure_ascii=False,indent=2),encoding="utf-8"); report["alv_decision_workflow"]=alv
 mandate_path=out/"alv-execution-mandates.json"
 try: existing_mandates=json.loads(mandate_path.read_text(encoding="utf-8"))
 except Exception: existing_mandates={}
 mandates=build_execution_mandates(alv,existing_mandates); compliance_before=evaluate_mandate_compliance(mandates); governed_mandates={**mandates,"mandates":compliance_before["mandates"],"compliance_status":compliance_before["status"]}; forecast_before=forecast_mandates(governed_mandates,warning_days=a.mandate_warning_days); optimizer=optimize_corrective_actions(forecast_before)
 corrective_path=out/"corrective-decision-workflow.json"
 try: existing_corrective=json.loads(corrective_path.read_text(encoding="utf-8"))
 except Exception: existing_corrective={}
 corrective=build_corrective_decisions(optimizer,existing_corrective); amendments=approved_mandate_amendments(corrective); corrective_path.write_text(json.dumps(corrective,ensure_ascii=False,indent=2),encoding="utf-8")
 amendment_path=out/"mandate-amendment-history.json"
 try: existing_amendment_history=json.loads(amendment_path.read_text(encoding="utf-8"))
 except Exception: existing_amendment_history={}
 amendment_result=apply_mandate_amendments(governed_mandates,amendments,existing_amendment_history); governed_mandates=amendment_result["mandates"]; compliance=evaluate_mandate_compliance(governed_mandates); governed_mandates={**governed_mandates,"mandates":compliance["mandates"],"compliance_status":compliance["status"]}; forecast=forecast_mandates(governed_mandates,warning_days=a.mandate_warning_days)
 effectiveness_path=out/"amendment-effectiveness-report.json"
 try: existing_effectiveness=json.loads(effectiveness_path.read_text(encoding="utf-8"))
 except Exception: existing_effectiveness={}
 effectiveness=evaluate_amendment_effectiveness(amendment_result,compliance_before,forecast_before,compliance,forecast,existing_effectiveness); effectiveness_path.write_text(json.dumps(effectiveness,ensure_ascii=False,indent=2),encoding="utf-8")
 governed_mandates.update(forecast_status=forecast['status'],corrective_action_status=optimizer['status'],corrective_approval_status=corrective['status'],approved_amendments=amendments,amendment_status=amendment_result['status'],amendment_effectiveness_status=effectiveness['status']); mandate_path.write_text(json.dumps(governed_mandates,ensure_ascii=False,indent=2),encoding="utf-8")
 report.update(alv_execution_mandates=governed_mandates,mandate_compliance_before=compliance_before,mandate_forecast_before=forecast_before,mandate_compliance=compliance,mandate_forecast=forecast,corrective_action_optimizer=optimizer,corrective_decision_workflow=corrective,approved_mandate_amendments=amendments,mandate_amendment=amendment_result,amendment_effectiveness=effectiveness)
 tower=build_control_tower(report); report['governance_control_tower']=tower; radar=build_risk_radar(report,months=a.risk_outlook_months); report['executive_risk_radar']=radar; scenario=build_strategic_scenario_radar(radar,tower); report['strategic_scenario_radar']=scenario
 strategy_path=out/'scenario-strategy-lock.json'
 try: existing_strategy=json.loads(strategy_path.read_text(encoding='utf-8'))
 except Exception: existing_strategy={}
 strategy=build_strategy_lock(scenario,existing_strategy); strategy_path.write_text(json.dumps(strategy,ensure_ascii=False,indent=2),encoding='utf-8'); report['scenario_strategy_lock']=strategy
 scorecard=build_strategy_execution_scorecard(strategy,report); report['strategy_execution_scorecard']=scorecard; intervention=build_strategy_interventions(scorecard,report); report['strategy_intervention_engine']=intervention; impact=simulate_intervention_impacts(intervention,report,discount_rate=a.discount_rate); report['intervention_impact_simulator']=impact; matrix=build_intervention_decision_matrix(impact,scorecard); report['intervention_decision_matrix']=matrix
 intervention_mandate_path=out/'intervention-execution-mandate.json'
 try: existing_intervention_mandate=json.loads(intervention_mandate_path.read_text(encoding='utf-8'))
 except Exception: existing_intervention_mandate={}
 intervention_mandate=build_intervention_execution_mandate(matrix,existing_intervention_mandate); intervention_mandate_path.write_text(json.dumps(intervention_mandate,ensure_ascii=False,indent=2),encoding='utf-8'); report['intervention_execution_mandate']=intervention_mandate
 benefits_path=out/'execution-benefits-tracking.json'
 try: existing_benefits=json.loads(benefits_path.read_text(encoding='utf-8'))
 except Exception: existing_benefits={}
 benefits=track_execution_and_benefits(intervention_mandate,report,existing_benefits); benefits_path.write_text(json.dumps(benefits,ensure_ascii=False,indent=2),encoding='utf-8'); report['execution_benefits_tracking']=benefits
 closed_loop=build_closed_loop_management(report); report['closed_loop_management']=closed_loop
 reports={"production-verification-report.json":report,"closed-loop-management.json":closed_loop,"closed-loop-dashboard.json":{"status":closed_loop['status'],"loop_completeness_score":closed_loop['loop_completeness_score'],"governance_safe":closed_loop['governance_safe'],"stages":closed_loop['stages'],"benefits_realization_score":closed_loop['benefits_realization_score'],"next_action":closed_loop['next_action']},"strategy-execution-scorecard.json":scorecard,"strategy-intervention-report.json":intervention,"intervention-impact-report.json":impact,"intervention-decision-matrix.json":matrix,"intervention-execution-dashboard.json":{"status":intervention_mandate['status'],"decision":intervention_mandate['decision'],"mandate":intervention_mandate['mandate'],"next_action":intervention_mandate['next_action']},"execution-benefits-dashboard.json":{"status":benefits['status'],"tracking":benefits['tracking'],"benefits":benefits['benefits'],"closure":benefits['closure'],"next_action":benefits['next_action']},"governance-control-tower.json":tower,"executive-risk-radar.json":radar,"strategic-scenario-radar.json":scenario,"scenario-strategy-dashboard.json":{"status":strategy['status'],"selected_scenario":strategy['selected_scenario'],"decision":strategy['decision'],"deviation":strategy['deviation'],"next_action":strategy['next_action']},"release-control-center.json":control,"reliability-sla-monitor.json":sla,"governance-dashboard.json":register["dashboard"]}
 for name,payload in reports.items(): (out/name).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({**report,"closed_loop_management_file":str(out/'closed-loop-management.json')},ensure_ascii=False,indent=2)); return 0 if tower['overall_status']!='ROOD' and scorecard['status']!='BUITEN KOERS' and closed_loop['governance_safe'] and autonomous.get("cycle_status")=="AUTONOOM GROEN" and not compliance.get("human_escalation_required") else 2
if __name__=="__main__": raise SystemExit(main())
