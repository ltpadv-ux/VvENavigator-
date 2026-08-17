#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from production_orchestrator import run_production_release
from production_verification import verify_production_result
from verification_diagnostics import diagnose_verification

def main()->int:
 p=argparse.ArgumentParser(description="VvE Navigator 4.2 Production Verification & Diagnostics")
 p.add_argument("dataset",nargs="?",default=str(ROOT/"data"/"sample_vve_34.json")); p.add_argument("--output",default=str(ROOT/"artifacts"/"verification")); p.add_argument("--horizon",type=int,default=30)
 a=p.parse_args(); release=run_production_release(a.dataset,a.output,horizon_years=a.horizon); verification=verify_production_result(release); diagnostics=diagnose_verification(verification,release)
 report={"release":release,"verification":verification,"diagnostics":diagnostics}; out=Path(a.output); out.mkdir(parents=True,exist_ok=True); report_path=out/"production-verification-report.json"; report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({**report,"verification_report":str(report_path)},ensure_ascii=False,indent=2)); return 0 if verification["verified"] else 2
if __name__=="__main__": raise SystemExit(main())
