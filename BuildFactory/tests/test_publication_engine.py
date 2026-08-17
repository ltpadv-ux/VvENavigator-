import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from publication_engine import build_publication_package


def test_publication_package():
    pack = {
        "pack_version": "3.2.0",
        "executive_summary": "Samenvatting",
        "board_report": {
            "management_summary": "Samenvatting",
            "kpis": {"decision_readiness": 88, "vni": 82},
            "board_decision": "Kies scenario Duurzaam",
            "top_actions": ["Actie 1", "Actie 2"],
        },
        "alv_decision_page": {
            "agenda_title": "Besluit voorkeursstrategie Duurzaam",
            "proposal": "Voorstel",
            "financial_consequence": "€200 p/m",
            "requested_decision": "Vaststellen / Aanpassen / Aanhouden",
        },
    }
    result = build_publication_package(pack, "DichterRijck", status="GEREED VOOR PUBLICATIE", publication_date="2026-08-17T17:30:00+00:00")
    assert result["status"] == "PUBLICATIEKLAAR"
    assert result["meta"]["vve_name"] == "DichterRijck"
    assert result["formats"]["pdf"]["render_ready"] is True
    assert "DichterRijck" in result["formats"]["html"]
