import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from document_renderer import build_render_model, render_html


def test_document_render_model_and_html():
    publication = {
        "meta": {"vve_name": "DichterRijck", "version": "3.4.0", "publication_date": "2026-08-17", "status": "CONCEPT"},
        "formats": {
            "excel": {"sheets": {
                "Executive Summary": [{"summary": "Samenvatting"}],
                "KPI": [{"vni": 82, "reserve": 223772.26}],
                "Board Decision": [{"decision": "Voer voorkeursstrategie uit"}],
                "Top Actions": [{"action": "Actie 1"}],
                "ALV Besluit": [{"agenda_title": "Strategie", "proposal": "Voorstel", "financial_consequence": "Beperkt", "requested_decision": "Vaststellen"}],
            }}
        },
    }
    model = build_render_model(publication)
    assert model["renderer_version"] == "3.4.0"
    assert len(model["sections"]) == 7
    html = render_html(model)
    assert "DichterRijck" in html
    assert "Kern-KPI" in html
