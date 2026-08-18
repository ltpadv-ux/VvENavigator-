#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
VERSION="7.0.0"; ROOT=Path(__file__).resolve().parent; CONFIG=ROOT/"config"/"navigator.json"
def load_config(): return json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
def cmd_version(): print(f"VvE Navigator BuildFactory {VERSION}"); return 0
def cmd_init():
 for d in (ROOT/"config",ROOT/"config"/"policies",ROOT/"src",ROOT/"tests",ROOT/"data",ROOT/"artifacts"): d.mkdir(parents=True,exist_ok=True)
 print("BuildFactory initialized"); return 0
def cmd_doctor():
 files=["closed_loop_management.py","execution_benefits_tracking.py","intervention_execution_mandate.py","intervention_decision_matrix.py","intervention_impact_simulator.py","strategy_intervention_engine.py","strategy_execution_scorecard.py","scenario_strategy_lock.py","strategic_scenario_radar.py","executive_risk_radar.py","governance_control_tower.py","amendment_effectiveness.py","mandate_amendment_engine.py","corrective_decision_workflow.py","mandate_forecast.py","mandate_compliance.py","alv_mandate_control.py","alv_decision_workflow.py","governance_decision_register.py","autonomous_governance.py","decision_intelligence.py","executive_cockpit.py","production_orchestrator.py","production_verification.py","self_healing.py","release_control_center.py","reliability_sla.py","enterprise_core.py","mjop_engine.py","finance_engine.py","financial_cockpit.py","risk_engine.py","governance_engine.py","audit_engine.py","compliance_engine.py","dashboard_engine.py","report_engine.py","datahub.py","excel_master.py","scenario_engine.py"]
 checks={"config":CONFIG.exists(),"requirements":(ROOT/"requirements.txt").exists(),"production_release_entrypoint":(ROOT/"run_production_release.py").exists(),"production_verification_entrypoint":(ROOT/"run_production_verification.py").exists(),**{f[:-3]:(ROOT/"src"/f).exists() for f in files},"standard_policy":(ROOT/"config"/"policies"/"standard_vve.json").exists(),"sample_vve_34":(ROOT/"data"/"sample_vve_34.json").exists()}
 for n,ok in checks.items(): print(f"[{'OK' if ok else 'FAIL'}] {n}")
 return 0 if all(checks.values()) else 1
def cmd_status():
 c=load_config(); keys=["project","closed_loop_management","execution_benefits_tracking","intervention_execution_mandate","intervention_decision_matrix","intervention_impact_simulator","strategy_intervention_engine","strategy_execution_scorecard","scenario_strategy_lock","enterprise","modules"]
 print(json.dumps({"version":VERSION,**{k:c.get(k,{}) for k in keys}},indent=2,ensure_ascii=False)); return 0
def main():
 p=argparse.ArgumentParser(); p.add_argument("command",choices=("init","doctor","version","status")); a=p.parse_args(); return {"init":cmd_init,"doctor":cmd_doctor,"version":cmd_version,"status":cmd_status}[a.command]()
if __name__=="__main__": raise SystemExit(main())
