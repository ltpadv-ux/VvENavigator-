"""Export adapters for the VvE Navigator DataHub."""
from __future__ import annotations

import csv
import io
import json
from typing import Any


def to_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


def to_csv(payload: dict[str, Any]) -> str:
    """Serialize normalized DataHub rows to a flat CSV."""
    rows = payload.get("rows", [])
    columns = payload.get("columns", ["entity", "year", "category", "value", "unit", "source"])
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()
