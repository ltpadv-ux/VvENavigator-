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

def main()->int:
 p=argparse.ArgumentParser(description="VvE Navigator 5.5 Mandate Forecast & Early Warning"); p.add_argument("dataset",nargs="?",default=str(ROOT/"data"/"sample_vve_34.json")); p.add_argument("--output",default=str(ROOT/"artifacts"/"verification")); p.add_argument("--horizon",type=int,default=30); p.add_argument("--self-heal",action="store_true",default=True); p.add_argument("--sla",type=float,default=95.0); p.add_argument("--closure-runs",type=int,default=3); p.add_argument("--mandate-warning-days",type=int,default=30); a=p.parse_args()
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
 mandates=build_execution_mandates(alv,existing_mandates); compliance=evaluate_mandate_compliance(mandates); governed_mandates={**mandates,"mandates":compliance["mandates"],"compliance_status":compliance["status"]}; forecast=forecast_mandates(governed_mandates,warning_days=a.mandate_warning_days); governed_mandates["forecast_status"]=forecast["status"]; mandate_path.write_text(json.dumps(governed_mandates,ensure_ascii=False,indent=2),encoding="utf-8"); report["alv_execution_mandates"]=governed_mandates; report["mandate_compliance"]=compliance; report["mandate_forecast"]=forecast
 reports={"production-verification-report.json":report,"release-control-center.json":control,"release-trend-monitor.json":trend,"reliability-sla-monitor.json":sla,"sla-improvement-report.json":improvement,"improvement-governance-report.json":governance,"autonomous-governance-report.json":autonomous,"governance-dashboard.json":register["dashboard"],"alv-decision-dashboard.json":{"status":alv["status"],"item_count":alv["item_count"],"ready_for_alv":alv["ready_for_alv"],"decided_count":alv["decided_count"],"next_action":alv["next_action"]},"alv-mandate-dashboard.json":{"status":governed_mandates["status"],"mandate_count":governed_mandates["mandate_count"],"open_count":governed_mandates["open_count"],"total_budget":governed_mandates["total_budget"],"total_spent":governed_mandates["total_spent"],"budget_remaining":governed_mandates["budget_remaining"],"compliance_status":compliance["status"],"forecast_status":forecast["status"],"high_risk":forecast["high_risk"],"medium_risk":forecast["medium_risk"],"next_action":forecast["next_action"] if forecast["status"]!="STABIEL" else compliance["next_action"]},"mandate-compliance-report.json":compliance,"mandate-forecast-report.json":forecast}
 for name,payload in reports.items(): (out/name).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({**report,"release_history":str(history_path),"improvement_backlog_file":str(backlog_path),"governance_decision_register_file":str(register_path),"alv_decision_workflow_file":str(alv_path),"alv_execution_mandates_file":str(mandate_path),"mandate_compliance_report":str(out/"mandate-compliance-report.json"),"mandate_forecast_report":str(out/"mandate-forecast-report.json")},ensure_ascii=False,indent=2)); return 0 if autonomous.get("cycle_status")=="AUTONOOM GROEN" and not compliance.get("human_escalation_required") else 2
if __name__=="__main__": raise SystemExit(main())
