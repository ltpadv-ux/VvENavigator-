#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
VERSION="14.3.0"; ROOT=Path(__file__).resolve().parent; CONFIG=ROOT/"config"/"navigator.json"
def load_config(): return json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
def cmd_version(): print(f"VvE Navigator BuildFactory {VERSION}"); return 0
def cmd_init():
 for d in (ROOT/"config",ROOT/"config"/"policies",ROOT/"src",ROOT/"tests",ROOT/"data",ROOT/"artifacts"): d.mkdir(parents=True,exist_ok=True)
 print("BuildFactory initialized"); return 0
def cmd_doctor():
 files=["financial_resolution_execution_mandate_budget_lock.py","alv_voting_quorum_financial_resolution_validation.py","board_decision_alv_financial_resolution_pack.py","integrated_financial_governance_decision_cockpit.py","contribution_path_stress_test_payment_shock.py","contribution_smoothing_multi_year_funding_optimizer.py","member_contribution_affordability_fairness.py","preventive_governance_funding_reserve_impact.py","constitutional_governance_control_tower.py","formal_resolution_voting_register.py","resolution_execution_compliance.py","finance_engine.py","mjop_engine.py","risk_engine.py","governance_engine.py","audit_engine.py","excel_master.py"]
 checks={"config":CONFIG.exists(),"requirements":(ROOT/"requirements.txt").exists(),**{f[:-3]:(ROOT/"src"/f).exists() for f in files},"standard_policy":(ROOT/"config"/"policies"/"standard_vve.json").exists(),"sample_vve_34":(ROOT/"data"/"sample_vve_34.json").exists()}
 for n,ok in checks.items(): print(f"[{'OK' if ok else 'FAIL'}] {n}")
 return 0 if all(checks.values()) else 1
def cmd_status():
 c=load_config(); keys=["project","financial_resolution_execution_mandate_budget_lock","alv_voting_quorum_financial_resolution_validation","board_decision_alv_financial_resolution_pack","integrated_financial_governance_decision_cockpit","enterprise","modules"]
 print(json.dumps({"version":VERSION,**{k:c.get(k,{}) for k in keys}},indent=2,ensure_ascii=False)); return 0
def main():
 p=argparse.ArgumentParser(); p.add_argument("command",choices=("init","doctor","version","status")); a=p.parse_args(); return {"init":cmd_init,"doctor":cmd_doctor,"version":cmd_version,"status":cmd_status}[a.command]()
if __name__=="__main__": raise SystemExit(main())
