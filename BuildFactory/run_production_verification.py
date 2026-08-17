#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from production_orchestrator import run_production_release
from production_verification import verify_production_result

def main()->int:
 p=argparse.ArgumentParser(description="VvE Navigator 4.1 Production Verification")
 p.add_argument("dataset",nargs="?",default=str(ROOT/"data"/"sample_vve_34.json")); p.add_argument("--output",default=str(ROOT/"artifacts"/"verification")); p.add_argument("--horizon",type=int,default=30)
 a=p.parse_args(); release=run_production_release(a.dataset,a.output,horizon_years=a.horizon); verification=verify_production_result(release); print(json.dumps({"release":release,"verification":verification},ensure_ascii=False,indent=2)); return 0 if verification["verified"] else 2
if __name__=="__main__": raise SystemExit(main())
