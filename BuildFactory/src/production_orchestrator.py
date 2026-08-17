"""End-to-end production release orchestrator for VvE Navigator 4.3."""
from __future__ import annotations
from pathlib import Path
from typing import Any
from enterprise_core import ReleaseProfile, run_enterprise
from executive_cockpit import build_executive_cockpit
from executive_reporting import build_executive_pack
from publication_engine import build_publication_package
from document_renderer import build_render_model
from native_export_engine import generate_native_export
from release_packaging import build_release_index, write_release_package
from release_validation import validate_release
ORCHESTRATOR_VERSION="4.3.0"
def _decision_layer(enterprise:dict[str,Any])->dict[str,Any]:
 release=enterprise.get("release",{}) or {}; quality=release.get("quality_gate",{}) or {}; ok=bool(quality.get("can_publish",False)); dash=release.get("dashboard",{}) or {}; actions=list(dash.get("top_actions",dash.get("actions",[])) or [])
 return {"status":"BESLUITRIJP" if ok else "HERZIEN","readiness_score":100.0 if ok else 40.0,"board_decision":"Leg het gevalideerde VvE Navigator-pakket ter besluitvorming voor aan de ALV." if ok else "Herstel blokkerende kwaliteitsissues vóór agendering.","key_metrics":{"deficit_probability":0.0,"monthly_per_apartment":0.0,"scenario":"Basis"},"blocking_reasons":[] if ok else ["Quality Gate blokkeert publicatie"],"actions":actions}
def run_production_release(dataset_path:str,output_dir:str|Path="artifacts",vve_name:str|None=None,horizon_years:int=30)->dict[str,Any]:
 enterprise=run_enterprise(dataset_path,ReleaseProfile(name="production-4.3",horizon_years=horizon_years))
 if enterprise.get("status")!="READY": return {"orchestrator_version":ORCHESTRATOR_VERSION,"status":"BLOCKED","enterprise":enterprise}
 release=enterprise.get("release",{}) or {}; dashboard=release.get("dashboard",{}) or {}; decision=_decision_layer(enterprise); cockpit=build_executive_cockpit(decision,dashboard=dashboard,financial={},health=enterprise.get("health",{})); pack=build_executive_pack(cockpit); name=vve_name or release.get("project") or Path(dataset_path).stem
 publication=build_publication_package(pack,name,version=ORCHESTRATOR_VERSION,status="GEREED VOOR PUBLICATIE"); model=build_render_model(publication); native=generate_native_export(model,output_dir); files={k:v for k,v in native.get("files",{}).items() if k in {"pdf","docx","xlsx","html"}}; index=build_release_index(ORCHESTRATOR_VERSION,name,files,status="GEREED VOOR ALV"); validation=validate_release(index,release.get("quality_gate",{})); package=write_release_package(ORCHESTRATOR_VERSION,name,files,output_dir,status=validation["status"])
 return {"orchestrator_version":ORCHESTRATOR_VERSION,"status":validation["status"],"enterprise":enterprise,"executive_cockpit":cockpit,"executive_pack":pack,"publication":publication,"render_model":model,"native_export":native,"release_index":index,"validation":validation,"package":package}
