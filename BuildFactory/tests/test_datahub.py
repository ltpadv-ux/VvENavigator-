import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from datahub import DataRow, export_payload, normalize_rows
from export_engine import to_csv, to_json


def test_normalize_rows():
    rows = normalize_rows([{"year": 2027, "category": "MJOP", "value": 1234.567}])
    assert rows[0]["value"] == 1234.57
    assert rows[0]["entity"] == "VvE"


def test_export_contract():
    payload = export_payload([DataRow("DichterRijck", 2027, "reserve", 100000)])
    assert payload["schema_version"] == "1.0"
    assert payload["row_count"] == 1
    assert "DichterRijck" in to_json(payload)
    assert "reserve" in to_csv(payload)
