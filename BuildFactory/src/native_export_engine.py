"""Native file export orchestration for VvE Navigator."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import json, zipfile
from .artifact_generator import build_artifact_plan, generate_html_artifact
from .binary_renderers import render_all
ENGINE_VERSION="3.7.0"

def build_native_export_contract(model:dict[str,Any],output_dir:str|Path="artifacts")->dict[str,Any]:
 plan=build_artifact_plan(model,output_dir); files=plan["files"]
 return {"native_export_version":ENGINE_VERSION,"status":"READY_TO_RENDER","files":files,"renderers":{"pdf":{"library":"reportlab","target":files["pdf"]},"docx":{"library":"python-docx","target":files["docx"]},"xlsx":{"library":"openpyxl","target":files["xlsx"]}},"distribution_zip":str(Path(output_dir)/(Path(files["html"]).stem+"-distribution.zip"))}

def package_existing_artifacts(contract:dict[str,Any])->dict[str,Any]:
 existing=[Path(p) for k,p in contract.get("files",{}).items() if k!="manifest" and Path(p).exists()]
 zip_path=Path(contract["distribution_zip"]); zip_path.parent.mkdir(parents=True,exist_ok=True)
 if existing:
  with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED) as zf:
   for p in existing: zf.write(p,arcname=p.name)
 return {**contract,"status":"PACKAGED" if existing else "NO_ARTIFACTS","packaged":[str(p) for p in existing],"zip":str(zip_path) if existing else ""}

def generate_native_export(model:dict[str,Any],output_dir:str|Path="artifacts")->dict[str,Any]:
 html=generate_html_artifact(model,output_dir); contract=build_native_export_contract(model,output_dir)
 generated={"html":html["files"]["html"]}
 try: generated.update(render_all(model,contract["files"])); binary_status="GENERATED"
 except ImportError as exc: binary_status=f"DEPENDENCY_ERROR: {exc}"
 manifest={"native_export_version":ENGINE_VERSION,"generated":generated,"binary_status":binary_status,"renderers":contract["renderers"]}
 Path(html["files"]["manifest"]).write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding="utf-8")
 result=package_existing_artifacts(contract); result["manifest"]=manifest; return result
