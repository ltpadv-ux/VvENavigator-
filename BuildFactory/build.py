#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
VERSION="4.1.0"; ROOT=Path(__file__).resolve().parent; CONFIG=ROOT/"config"/"navigator.json"
def load_config(): return json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
def cmd_version(): print(f"VvE Navigator BuildFactory {VERSION}"); return 0
def cmd_init():
 for d in (ROOT/"config",ROOT/"config"/"policies",ROOT/"src",ROOT/"tests",ROOT/"data",ROOT/"artifacts"): d.mkdir(parents=True,exist_ok=True)
 print("BuildFactory initialized"); return 0
def cmd_doctor():
 files=["decision_intelligence.py","executive_cockpit.py","executive_reporting.py","publication_engine.py","document_renderer.py","artifact_generator.py","native_export_engine.py","binary_renderers.py","release_packaging.py","release_validation.py","production_orchestrator.py","production_verification.py","enterprise_core.py","release_manifest.py","health_engine.py","policy_engine.py","portfolio_engine.py","forecast_engine.py","stress_engine.py","optimization_engine.py","strategy_optimizer.py","recommendation_engine.py","mjop_engine.py","finance_engine.py","financial_cockpit.py","risk_engine.py","decision_engine.py","governance_engine.py","action_engine.py","audit_engine.py","compliance_engine.py","release_engine.py","dashboard_engine.py","report_engine.py","datahub.py","export_engine.py","excel_master.py","navigator_mvp.py","scenario_engine.py","practice_dataset.py"]
 checks={"config":CONFIG.exists(),"requirements":(ROOT/"requirements.txt").exists(),"production_release_entrypoint":(ROOT/"run_production_release.py").exists(),"production_verification_entrypoint":(ROOT/"run_production_verification.py").exists(),**{f[:-3]:(ROOT/"src"/f).exists() for f in files},"standard_policy":(ROOT/"config"/"policies"/"standard_vve.json").exists(),"sample_vve_34":(ROOT/"data"/"sample_vve_34.json").exists()}
 for n,ok in checks.items(): print(f"[{'OK' if ok else 'FAIL'}] {n}")
 return 0 if all(checks.values()) else 1
def cmd_status():
 c=load_config(); keys=["project","production_orchestrator","production_verification","decision_intelligence","executive_cockpit","executive_reporting","publication","document_rendering","artifact_generation","native_export","binary_renderers","release_packaging","release_validation","enterprise","health","policy","portfolio","forecast","stress_test","optimization","strategy_optimizer","recommendation","modules"]
 print(json.dumps({"version":VERSION,**{k:c.get(k,{}) for k in keys}},indent=2,ensure_ascii=False)); return 0
def main():
 p=argparse.ArgumentParser(); p.add_argument("command",choices=("init","doctor","version","status")); a=p.parse_args(); return {"init":cmd_init,"doctor":cmd_doctor,"version":cmd_version,"status":cmd_status}[a.command]()
if __name__=="__main__": raise SystemExit(main())
