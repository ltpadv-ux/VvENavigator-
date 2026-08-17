#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from production_orchestrator import run_production_release

def main()->int:
 p=argparse.ArgumentParser(description="VvE Navigator 4.0 Production Release Orchestrator")
 p.add_argument("dataset",nargs="?",default=str(ROOT/"data"/"sample_vve_34.json")); p.add_argument("--output",default=str(ROOT/"artifacts")); p.add_argument("--vve-name",default=None); p.add_argument("--horizon",type=int,default=30)
 a=p.parse_args(); result=run_production_release(a.dataset,a.output,a.vve_name,a.horizon); print(json.dumps(result,ensure_ascii=False,indent=2)); return 0 if result.get("status")=="VRIJGEGEVEN VOOR ALV" else 2
if __name__=="__main__": raise SystemExit(main())
