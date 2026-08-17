"""Publication engine for VvE Navigator executive packs."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from html import escape
from typing import Any


@dataclass(frozen=True)
class PublicationMeta:
    vve_name: str
    version: str
    publication_date: str
    status: str
    source: str = "Executive Reporting & ALV Pack"


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _validate_status(status: str) -> str:
    allowed = {"CONCEPT", "TER CONTROLE", "GEREED VOOR PUBLICATIE", "GEPUBLICEERD"}
    value = str(status).upper()
    if value not in allowed:
        raise ValueError(f"publication status must be one of: {sorted(allowed)}")
    return value


def to_html_document(executive_pack: dict[str, Any], meta: PublicationMeta) -> str:
    """Render a standalone HTML report suitable for browser/PDF conversion."""
    board = executive_pack.get("board_report", {}) or {}
    alv = executive_pack.get("alv_decision_page", {}) or {}
    kpis = board.get("kpis", {}) or {}
    actions = board.get("top_actions", []) or []
    rows = "".join(
        f"<tr><th>{escape(str(key))}</th><td>{escape(str(value))}</td></tr>" for key, value in kpis.items()
    )
    action_items = "".join(f"<li>{escape(str(item))}</li>" for item in actions)
    return f"""<!doctype html>
<html lang=\"nl\">
<head><meta charset=\"utf-8\"><title>{escape(meta.vve_name)} - VvE Navigator</title></head>
<body>
<header>
<h1>VvE Navigator - Executive Publicatie</h1>
<p><strong>VvE:</strong> {escape(meta.vve_name)} | <strong>Versie:</strong> {escape(meta.version)} | <strong>Status:</strong> {escape(meta.status)}</p>
<p><strong>Publicatiedatum:</strong> {escape(meta.publication_date)}</p>
</header>
<section><h2>Managementsamenvatting</h2><p>{escape(str(board.get('management_summary', '')))}</p></section>
<section><h2>Kern-KPI's</h2><table>{rows}</table></section>
<section><h2>Bestuursbesluit</h2><p>{escape(str(board.get('board_decision', '')))}</p></section>
<section><h2>Topacties</h2><ol>{action_items}</ol></section>
<section><h2>ALV-besluitpagina</h2>
<h3>{escape(str(alv.get('agenda_title', '')))}</h3>
<p>{escape(str(alv.get('proposal', '')))}</p>
<p><strong>Financiële consequentie:</strong> {escape(str(alv.get('financial_consequence', '')))}</p>
<p><strong>Gevraagd besluit:</strong> {escape(str(alv.get('requested_decision', '')))}</p>
</section>
</body></html>"""


def excel_export_contract(executive_pack: dict[str, Any], meta: PublicationMeta) -> dict[str, Any]:
    """Create a workbook-neutral contract for Excel export."""
    board = executive_pack.get("board_report", {}) or {}
    alv = executive_pack.get("alv_decision_page", {}) or {}
    return {
        "meta": asdict(meta),
        "sheets": {
            "Executive Summary": [{"summary": executive_pack.get("executive_summary", "")}],
            "KPI": [board.get("kpis", {})],
            "Board Decision": [{"decision": board.get("board_decision", "")}],
            "Top Actions": [{"action": item} for item in board.get("top_actions", []) or []],
            "ALV Besluit": [alv],
        },
    }


def build_publication_package(
    executive_pack: dict[str, Any],
    vve_name: str,
    version: str = "3.3.0",
    status: str = "CONCEPT",
    publication_date: str | None = None,
) -> dict[str, Any]:
    """Create publication-ready HTML/PDF/Excel structures from one executive pack."""
    if not executive_pack:
        return {"status": "ONVOLLEDIG", "meta": {}, "formats": {}}
    validated_status = _validate_status(status)
    meta = PublicationMeta(
        vve_name=str(vve_name).strip() or "Onbekende VvE",
        version=str(version),
        publication_date=publication_date or _iso_now(),
        status=validated_status,
    )
    html = to_html_document(executive_pack, meta)
    return {
        "publication_engine_version": "3.3.0",
        "status": "PUBLICATIEKLAAR" if validated_status in {"GEREED VOOR PUBLICATIE", "GEPUBLICEERD"} else validated_status,
        "meta": asdict(meta),
        "formats": {
            "html": html,
            "pdf": {
                "source_format": "html",
                "render_ready": True,
                "document_title": f"{meta.vve_name} - VvE Navigator {meta.version}",
            },
            "excel": excel_export_contract(executive_pack, meta),
        },
        "source_pack_version": executive_pack.get("pack_version", ""),
    }
