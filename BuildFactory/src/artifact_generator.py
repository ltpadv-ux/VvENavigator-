"""Artifact generation contracts for VvE Navigator."""
from __future__ import annotations
import json, re
from pathlib import Path
from typing import Any
from .document_renderer import render_html

def _safe(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", str(value).strip()).strip("-") or "vve-navigator"

def build_artifact_plan(model: dict[str, Any], output_dir: str | Path = "artifacts") -> dict[str, Any]:
    meta = model.get("meta", {}) or {}
    base = _safe(f"{meta.get('vve_name','VvE')}-VvE-Navigator-{meta.get('version','3.5.0')}")
    root = Path(output_dir)
    return {"artifact_engine_version":"3.5.0","output_dir":str(root),"status":"PLANNED","files":{ext:str(root/f"{base}.{ext}") for ext in ("html","pdf","docx","xlsx")}|{"manifest":str(root/f"{base}.manifest.json")}}

def generate_html_artifact(model: dict[str, Any], output_dir: str | Path = "artifacts") -> dict[str, Any]:
    plan = build_artifact_plan(model, output_dir); root = Path(plan["output_dir"]); root.mkdir(parents=True, exist_ok=True)
    Path(plan["files"]["html"]).write_text(render_html(model), encoding="utf-8")
    manifest={"engine_version":"3.5.0","document_title":model.get("document_title","VvE Navigator"),"meta":model.get("meta",{}),"generated":{"html":plan["files"]["html"]},"pending_renderers":["PDF","DOCX","XLSX"],"source_renderer_version":model.get("renderer_version","")}
    Path(plan["files"]["manifest"]).write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding="utf-8")
    plan.update(status="HTML_GENERATED",manifest=manifest); return plan

def artifact_contract(model: dict[str, Any], output_dir: str | Path = "artifacts") -> dict[str, Any]:
    plan=build_artifact_plan(model,output_dir)
    return {**plan,"render_model":model,"adapters":{"pdf":{"page_size":model.get("page_plan",{}).get("page_size","A4")},"docx":{"sections":len(model.get("sections",[]))},"xlsx":{"sheets":["Executive Summary","KPI","Board Decision","Top Actions","ALV Besluit"]}}}
