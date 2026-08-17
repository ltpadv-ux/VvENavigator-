"""Document rendering contracts for VvE Navigator publications."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class RenderTheme:
    name: str = "VvE Navigator Executive"
    primary_color: str = "#1F4E78"
    accent_color: str = "#70AD47"
    font_family: str = "Aptos"
    page_size: str = "A4"


def build_render_model(publication_package: dict[str, Any], theme: RenderTheme | None = None) -> dict[str, Any]:
    """Create a renderer-neutral document model for PDF/HTML/Word style outputs."""
    theme = theme or RenderTheme()
    meta = publication_package.get("meta", {}) or {}
    formats = publication_package.get("formats", {}) or {}
    excel = formats.get("excel", {}) or {}
    sheets = excel.get("sheets", {}) or {}

    executive = (sheets.get("Executive Summary") or [{}])[0]
    kpi = (sheets.get("KPI") or [{}])[0]
    decision = (sheets.get("Board Decision") or [{}])[0]
    actions = sheets.get("Top Actions") or []
    alv = (sheets.get("ALV Besluit") or [{}])[0]

    sections = [
        {"id": "cover", "title": "VvE Navigator", "type": "cover", "content": {"vve_name": meta.get("vve_name", ""), "version": meta.get("version", ""), "publication_date": meta.get("publication_date", ""), "status": meta.get("status", "")}},
        {"id": "toc", "title": "Inhoudsopgave", "type": "toc", "content": ["Managementsamenvatting", "Kern-KPI's", "Bestuursbesluit", "Topacties", "ALV-besluitpagina"]},
        {"id": "summary", "title": "Managementsamenvatting", "type": "text", "content": executive.get("summary", "")},
        {"id": "kpis", "title": "Kern-KPI's", "type": "table", "content": [{"kpi": key, "value": value} for key, value in kpi.items()]},
        {"id": "decision", "title": "Bestuursbesluit", "type": "text", "content": decision.get("decision", "")},
        {"id": "actions", "title": "Topacties", "type": "list", "content": [item.get("action", "") for item in actions]},
        {"id": "alv", "title": "ALV-besluitpagina", "type": "decision_page", "content": alv},
    ]

    return {
        "renderer_version": "3.4.0",
        "document_title": f"{meta.get('vve_name', 'VvE')} - VvE Navigator",
        "theme": asdict(theme),
        "meta": meta,
        "sections": sections,
        "page_plan": {
            "page_size": theme.page_size,
            "include_page_numbers": True,
            "include_header": True,
            "include_footer": True,
            "include_toc": True,
        },
        "output_targets": ["HTML", "PDF", "DOCX"],
    }


def render_html(render_model: dict[str, Any]) -> str:
    """Render the neutral document model to styled standalone HTML."""
    theme = render_model.get("theme", {}) or {}
    meta = render_model.get("meta", {}) or {}
    sections = render_model.get("sections", []) or []
    body: list[str] = []
    for section in sections:
        title = section.get("title", "")
        content = section.get("content", "")
        kind = section.get("type")
        if kind == "cover":
            body.append(f"<section class='cover'><h1>VvE Navigator</h1><h2>{content.get('vve_name','')}</h2><p>Versie {content.get('version','')} · {content.get('publication_date','')} · {content.get('status','')}</p></section>")
        elif kind == "toc":
            body.append("<section><h2>Inhoudsopgave</h2><ol>" + "".join(f"<li>{item}</li>" for item in content) + "</ol></section>")
        elif kind == "table":
            rows = "".join(f"<tr><th>{row['kpi']}</th><td>{row['value']}</td></tr>" for row in content)
            body.append(f"<section><h2>{title}</h2><table>{rows}</table></section>")
        elif kind == "list":
            body.append(f"<section><h2>{title}</h2><ol>" + "".join(f"<li>{item}</li>" for item in content) + "</ol></section>")
        elif kind == "decision_page":
            body.append(f"<section><h2>{title}</h2><h3>{content.get('agenda_title','')}</h3><p>{content.get('proposal','')}</p><p><strong>Financiële consequentie:</strong> {content.get('financial_consequence','')}</p><p><strong>Gevraagd besluit:</strong> {content.get('requested_decision','')}</p></section>")
        else:
            body.append(f"<section><h2>{title}</h2><p>{content}</p></section>")

    return f"""<!doctype html><html lang='nl'><head><meta charset='utf-8'><title>{render_model.get('document_title','VvE Navigator')}</title><style>
body{{font-family:{theme.get('font_family','Aptos')},Arial,sans-serif;margin:40px;color:#222;line-height:1.45}}h1,h2,h3{{color:{theme.get('primary_color','#1F4E78')}}}.cover{{min-height:75vh;display:flex;flex-direction:column;justify-content:center;border-bottom:8px solid {theme.get('accent_color','#70AD47')}}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ccc;padding:8px;text-align:left}}section{{page-break-after:auto;margin-bottom:32px}}@media print{{.cover{{page-break-after:always}}section{{break-inside:avoid}}}}</style></head><body>{''.join(body)}<footer><small>{meta.get('vve_name','')} · VvE Navigator {meta.get('version','')}</small></footer></body></html>"""
