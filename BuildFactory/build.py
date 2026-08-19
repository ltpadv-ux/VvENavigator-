#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
VERSION="8.8.0"; ROOT=Path(__file__).resolve().parent; CONFIG=ROOT/"config"/"navigator.json"
def load_config(): return json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
def cmd_version(): print(f"VvE Navigator BuildFactory {VERSION}"); return 0
def cmd_init():
 for d in (ROOT/"config",ROOT/"config"/"policies",ROOT/"src",ROOT/"tests",ROOT/"data",ROOT/"artifacts"): d.mkdir(parents=True,exist_ok=True)
 print("BuildFactory initialized"); return 0
def cmd_doctor():
 files=["governance_maturity_index.py","audit_remediation_engine.py","treasury_audit_assurance.py","treasury_audit_lineage.py","treasury_decision_effectiveness.py","treasury_accountability_register.py","treasury_decision_board_pack.py","treasury_early_warning_calendar.py","portfolio_treasury_control_tower.py","treasury_recovery_effectiveness.py","treasury_recovery_mandate.py","treasury_stress_intervention.py","treasury_forecast.py","portfolio_liquidity_debt_control.py","portfolio_funding_covenant_control.py","portfolio_funding_strategy.py","portfolio_capital_allocation.py","portfolio_intelligence.py","closed_loop_management.py","production_orchestrator.py","production_verification.py","enterprise_core.py","mjop_engine.py","finance_engine.py","financial_cockpit.py","risk_engine.py","governance_engine.py","audit_engine.py","compliance_engine.py","dashboard_engine.py","report_engine.py","datahub.py","excel_master.py","scenario_engine.py"]
 checks={"config":CONFIG.exists(),"requirements":(ROOT/"requirements.txt").exists(),**{f[:-3]:(ROOT/"src"/f).exists() for f in files},"standard_policy":(ROOT/"config"/"policies"/"standard_vve.json").exists(),"sample_vve_34":(ROOT/"data"/"sample_vve_34.json").exists()}
 for n,ok in checks.items(): print(f"[{'OK' if ok else 'FAIL'}] {n}")
 return 0 if all(checks.values()) else 1
def cmd_status():
 c=load_config(); keys=["project","governance_maturity_index","audit_remediation","treasury_audit_assurance","portfolio_treasury_control_tower","closed_loop_management","enterprise","modules"]
 print(json.dumps({"version":VERSION,**{k:c.get(k,{}) for k in keys}},indent=2,ensure_ascii=False)); return 0
def main():
 p=argparse.ArgumentParser(); p.add_argument("command",choices=("init","doctor","version","status")); a=p.parse_args(); return {"init":cmd_init,"doctor":cmd_doctor,"version":cmd_version,"status":cmd_status}[a.command]()
if __name__=="__main__": raise SystemExit(main())
