"""Native file export orchestration for VvE Navigator."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import json, zipfile
from .artifact_generator import build_artifact_plan, generate_html_artifact

ENGINE_VERSION="3.6.0"

def build_native_export_contract(model: dict[str,Any], output_dir: str|Path="artifacts") -> dict[str,Any]:
    plan=build_artifact_plan(model,output_dir)
    files=plan["files"]
    return {"native_export_version":ENGINE_VERSION,"status":"READY_TO_RENDER","files":files,"renderers":{
        "pdf":{"library":"reportlab","target":files["pdf"],"source":"render_model"},
        "docx":{"library":"python-docx","target":files["docx"],"source":"render_model"},
        "xlsx":{"library":"openpyxl","target":files["xlsx"],"source":"render_model"}},
        "distribution_zip":str(Path(output_dir)/(Path(files["html"]).stem+"-distribution.zip"))}

def package_existing_artifacts(contract: dict[str,Any]) -> dict[str,Any]:
    """Bundle generated artifacts without pretending missing binary files exist."""
    targets=contract.get("files",{}); existing=[Path(p) for k,p in targets.items() if k!="manifest" and Path(p).exists()]
    zip_path=Path(contract["distribution_zip"]); zip_path.parent.mkdir(parents=True,exist_ok=True)
    if existing:
        with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED) as zf:
            for p in existing: zf.write(p,arcname=p.name)
    return {**contract,"status":"PACKAGED" if existing else "NO_ARTIFACTS","packaged":[str(p) for p in existing],"zip":str(zip_path) if existing else ""}

def generate_native_export(model: dict[str,Any], output_dir: str|Path="artifacts") -> dict[str,Any]:
    """Generate HTML now and expose explicit native adapters for PDF/DOCX/XLSX."""
    html=generate_html_artifact(model,output_dir)
    contract=build_native_export_contract(model,output_dir)
    manifest={"native_export_version":ENGINE_VERSION,"html":html["files"]["html"],"native_targets":contract["renderers"],"binary_status":"ADAPTERS_READY"}
    Path(html["files"]["manifest"]).write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding="utf-8")
    return package_existing_artifacts(contract)
