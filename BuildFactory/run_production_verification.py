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
from autonomous_governance import build_governance_cycle

def main()->int:
 p=argparse.ArgumentParser(description="VvE Navigator 5.0 Autonomous Governance Platform")
 p.add_argument("dataset",nargs="?",default=str(ROOT/"data"/"sample_vve_34.json")); p.add_argument("--output",default=str(ROOT/"artifacts"/"verification")); p.add_argument("--horizon",type=int,default=30); p.add_argument("--self-heal",action="store_true",default=True); p.add_argument("--sla",type=float,default=95.0); p.add_argument("--closure-runs",type=int,default=3)
 a=p.parse_args(); release=run_production_release(a.dataset,a.output,horizon_years=a.horizon); verification=verify_production_result(release); diagnostics=diagnose_verification(verification,release); healing=run_self_healing(release,max_attempts=1) if a.self_heal and not verification.get("verified") else {"status":"NOT_NEEDED","after":verification,"escalation_required":False,"repairs":[],"human_actions":[]}
 final_verification=healing.get("after",verification); final_diagnostics=diagnose_verification(final_verification,release); report={"release":release,"verification":final_verification,"diagnostics":final_diagnostics,"self_healing":healing}; control=build_release_control_center(report); report["control_center"]=control
 out=Path(a.output); out.mkdir(parents=True,exist_ok=True); history_path=out/"release-history.json"; trend=append_history(history_path,report); sla=evaluate_reliability_sla(trend,minimum_reliability=a.sla,max_blocked_recent=1)
 try: history=json.loads(history_path.read_text(encoding="utf-8"))
 except Exception: history=[]
 improvement=analyze_sla_root_causes(history,[final_diagnostics]); backlog_path=out/"continuous-improvement-backlog.json"; backlog=update_backlog_file(backlog_path,improvement); governance=govern_improvement_closure(backlog,history,sla,improvement,required_stable_runs=a.closure_runs)
 governed_backlog={**backlog,"items":governance["items"],"open_count":governance["open_count"],"status":"BIJGEWERKT" if governance["open_count"]==0 else "ACTIE VEREIST","next_action":governance["next_action"]}; backlog_path.write_text(json.dumps(governed_backlog,ensure_ascii=False,indent=2),encoding="utf-8")
 report.update(trend_monitor=trend,reliability_sla=sla,sla_improvement=improvement,improvement_backlog=governed_backlog,improvement_governance=governance); autonomous=build_governance_cycle(report); report["autonomous_governance"]=autonomous
 paths={"verification_report":out/"production-verification-report.json","control_center_report":out/"release-control-center.json","trend_report":out/"release-trend-monitor.json","sla_report":out/"reliability-sla-monitor.json","improvement_report":out/"sla-improvement-report.json","improvement_governance_report":out/"improvement-governance-report.json","autonomous_governance_report":out/"autonomous-governance-report.json"}
 payloads={"verification_report":report,"control_center_report":control,"trend_report":trend,"sla_report":sla,"improvement_report":improvement,"improvement_governance_report":governance,"autonomous_governance_report":autonomous}
 for key,path in paths.items(): path.write_text(json.dumps(payloads[key],ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({**report,"release_history":str(history_path),"improvement_backlog_file":str(backlog_path),**{k:str(v) for k,v in paths.items()}},ensure_ascii=False,indent=2)); return 0 if autonomous.get("cycle_status")=="AUTONOOM GROEN" else 2
if __name__=="__main__": raise SystemExit(main())
