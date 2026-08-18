#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
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

def main()->int:
 p=argparse.ArgumentParser(description="VvE Navigator 4.9 Production Verification & Improvement Governance")
 p.add_argument("dataset",nargs="?",default=str(ROOT/"data"/"sample_vve_34.json")); p.add_argument("--output",default=str(ROOT/"artifacts"/"verification")); p.add_argument("--horizon",type=int,default=30); p.add_argument("--self-heal",action="store_true",default=True); p.add_argument("--sla",type=float,default=95.0); p.add_argument("--closure-runs",type=int,default=3)
 a=p.parse_args(); release=run_production_release(a.dataset,a.output,horizon_years=a.horizon); verification=verify_production_result(release); diagnostics=diagnose_verification(verification,release); healing=run_self_healing(release,max_attempts=1) if a.self_heal and not verification.get("verified") else {"status":"NOT_NEEDED","after":verification,"escalation_required":False,"repairs":[],"human_actions":[]}
 final_verification=healing.get("after",verification); final_diagnostics=diagnose_verification(final_verification,release); report={"release":release,"verification":final_verification,"diagnostics":final_diagnostics,"self_healing":healing}; control=build_release_control_center(report); report["control_center"]=control
 out=Path(a.output); out.mkdir(parents=True,exist_ok=True); history_path=out/"release-history.json"; trend=append_history(history_path,report); sla=evaluate_reliability_sla(trend,minimum_reliability=a.sla,max_blocked_recent=1)
 try: history=json.loads(history_path.read_text(encoding="utf-8"))
 except Exception: history=[]
 improvement=analyze_sla_root_causes(history,[final_diagnostics]); backlog_path=out/"continuous-improvement-backlog.json"; backlog=update_backlog_file(backlog_path,improvement); governance=govern_improvement_closure(backlog,history,sla,improvement,required_stable_runs=a.closure_runs)
 governed_backlog={**backlog,"items":governance["items"],"open_count":governance["open_count"],"status":"BIJGEWERKT" if governance["open_count"]==0 else "ACTIE VEREIST","next_action":governance["next_action"]}; backlog_path.write_text(json.dumps(governed_backlog,ensure_ascii=False,indent=2),encoding="utf-8")
 report["trend_monitor"]=trend; report["reliability_sla"]=sla; report["sla_improvement"]=improvement; report["improvement_backlog"]=governed_backlog; report["improvement_governance"]=governance
 report_path=out/"production-verification-report.json"; control_path=out/"release-control-center.json"; trend_path=out/"release-trend-monitor.json"; sla_path=out/"reliability-sla-monitor.json"; improvement_path=out/"sla-improvement-report.json"; governance_path=out/"improvement-governance-report.json"
 report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8"); control_path.write_text(json.dumps(control,ensure_ascii=False,indent=2),encoding="utf-8"); trend_path.write_text(json.dumps(trend,ensure_ascii=False,indent=2),encoding="utf-8"); sla_path.write_text(json.dumps(sla,ensure_ascii=False,indent=2),encoding="utf-8"); improvement_path.write_text(json.dumps(improvement,ensure_ascii=False,indent=2),encoding="utf-8"); governance_path.write_text(json.dumps(governance,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({**report,"verification_report":str(report_path),"control_center_report":str(control_path),"release_history":str(history_path),"trend_report":str(trend_path),"sla_report":str(sla_path),"improvement_report":str(improvement_path),"improvement_backlog":str(backlog_path),"improvement_governance_report":str(governance_path)},ensure_ascii=False,indent=2)); return 0 if control.get("status") in {"GROEN","HERSTELD"} and sla.get("compliant") else 2
if __name__=="__main__": raise SystemExit(main())
