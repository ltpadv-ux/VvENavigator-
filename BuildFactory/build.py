#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
VERSION="12.9.0"; ROOT=Path(__file__).resolve().parent; CONFIG=ROOT/"config"/"navigator.json"
def load_config(): return json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
def cmd_version(): print(f"VvE Navigator BuildFactory {VERSION}"); return 0
def cmd_init():
 for d in (ROOT/"config",ROOT/"config"/"policies",ROOT/"src",ROOT/"tests",ROOT/"data",ROOT/"artifacts"): d.mkdir(parents=True,exist_ok=True)
 print("BuildFactory initialized"); return 0
def cmd_doctor():
 files=["post_activation_assurance_rollback_control.py","constitutional_activation_cutover_control.py","constitutional_impact_migration_control.py","constitutional_version_ledger.py","constitutional_remediation_amendment_register.py","constitutional_debt_remediation.py","waiver_monitoring_constitutional_debt.py","constitutional_exception_waiver_register.py","constitutional_compliance_gatekeeper.py","governance_constitution_control_framework.py","governance_policy_baseline_doctrine.py","governance_policy_drift_detection.py","precedent_aware_decision_consistency.py","institutional_memory_precedent_intelligence.py","governance_archive_memory.py","resolution_closure_governance_discharge.py","resolution_execution_compliance.py","formal_resolution_voting_register.py","board_decision_alv_pack.py","explainable_governance_ai.py","executive_command_center.py","executive_digital_twin.py","vve_governance_operating_system.py","finance_engine.py","mjop_engine.py","risk_engine.py","governance_engine.py","audit_engine.py","excel_master.py"]
 checks={"config":CONFIG.exists(),"requirements":(ROOT/"requirements.txt").exists(),**{f[:-3]:(ROOT/"src"/f).exists() for f in files},"standard_policy":(ROOT/"config"/"policies"/"standard_vve.json").exists(),"sample_vve_34":(ROOT/"data"/"sample_vve_34.json").exists()}
 for n,ok in checks.items(): print(f"[{'OK' if ok else 'FAIL'}] {n}")
 return 0 if all(checks.values()) else 1
def cmd_status():
 c=load_config(); keys=["project","post_activation_assurance_rollback_control","constitutional_activation_cutover_control","constitutional_impact_migration_control","constitutional_version_ledger","constitutional_remediation_amendment_register","constitutional_debt_remediation","constitutional_compliance_gatekeeper","governance_constitution_control_framework","executive_command_center","enterprise","modules"]
 print(json.dumps({"version":VERSION,**{k:c.get(k,{}) for k in keys}},indent=2,ensure_ascii=False)); return 0
def main():
 p=argparse.ArgumentParser(); p.add_argument("command",choices=("init","doctor","version","status")); a=p.parse_args(); return {"init":cmd_init,"doctor":cmd_doctor,"version":cmd_version,"status":cmd_status}[a.command]()
if __name__=="__main__": raise SystemExit(main())
