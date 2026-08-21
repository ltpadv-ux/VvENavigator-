#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
VERSION="17.5.0"; ROOT=Path(__file__).resolve().parent; CONFIG=ROOT/"config"/"navigator.json"
def load_config(): return json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
def cmd_version(): print(f"VvE Navigator BuildFactory {VERSION}"); return 0
def cmd_init():
 for d in (ROOT/"config",ROOT/"config"/"policies",ROOT/"src",ROOT/"tests",ROOT/"data",ROOT/"artifacts"): d.mkdir(parents=True,exist_ok=True)
 print("BuildFactory initialized"); return 0
def cmd_doctor():
 files=["ci_workflow_verification_evidence_harvesting.py","production_evidence_runner_rc1_closure_pack.py","rc1_evidence_closure_final_go_no_go.py","final_production_validation_rc1.py","production_release_candidate_go_no_go.py","security_access_release_hardening_gate.py","backup_restore_data_integrity_disaster_recovery.py","automated_regression_matrix_ci_evidence_gate.py","end_to_end_integration_quality_gate.py","model_drift_root_cause_recalibration.py","post_promotion_stability_model_drift_watchdog.py","controlled_model_promotion_version_freeze_rollback.py","shadow_run_live_parallel_validation.py","model_champion_challenger_validation.py","model_backtesting_forecast_accuracy_scorecard.py","autonomous_governance_learning_loop.py","baseline_breach_diagnosis_corrective_action.py","scenario_activation_baseline_monitoring_covenant.py","probability_aware_scenario_risk_appetite.py","digital_twin_scenario_probability_monte_carlo.py","adaptive_vve_financial_digital_twin.py","integrated_financial_governance_decision_cockpit.py","finance_engine.py","mjop_engine.py","risk_engine.py","governance_engine.py","audit_engine.py","excel_master.py"]
 checks={"config":CONFIG.exists(),"requirements":(ROOT/"requirements.txt").exists(),"enterprise_ci":(ROOT.parent/".github"/"workflows"/"enterprise-ci.yml").exists(),**{f[:-3]:(ROOT/"src"/f).exists() for f in files},"standard_policy":(ROOT/"config"/"policies"/"standard_vve.json").exists(),"sample_vve_34":(ROOT/"data"/"sample_vve_34.json").exists()}
 for n,ok in checks.items(): print(f"[{'OK' if ok else 'FAIL'}] {n}")
 return 0 if all(checks.values()) else 1
def cmd_status():
 c=load_config(); keys=["project","ci_workflow_verification_evidence_harvesting","production_evidence_runner_rc1_closure_pack","rc1_evidence_closure_final_go_no_go","enterprise","release","modules"]
 print(json.dumps({"version":VERSION,**{k:c.get(k,{}) for k in keys}},indent=2,ensure_ascii=False)); return 0
def main():
 p=argparse.ArgumentParser(); p.add_argument("command",choices=("init","doctor","version","status")); a=p.parse_args(); return {"init":cmd_init,"doctor":cmd_doctor,"version":cmd_version,"status":cmd_status}[a.command]()
if __name__=="__main__": raise SystemExit(main())
