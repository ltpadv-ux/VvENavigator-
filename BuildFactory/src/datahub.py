"""Normalized DataHub and export payloads for the VvE Navigator."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Iterable


@dataclass(frozen=True)
class DataRow:
    entity: str
    year: int
    category: str
    value: float
    unit: str = "EUR"
    source: str = "engine"


def normalize_rows(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize engine output into a flat, Power BI-friendly schema."""
    result: list[dict[str, Any]] = []
    for row in rows:
        result.append({
            "entity": str(row.get("entity", "VvE")),
            "year": int(row["year"]),
            "category": str(row.get("category", "unknown")),
            "value": round(float(row.get("value", 0.0)), 2),
            "unit": str(row.get("unit", "EUR")),
            "source": str(row.get("source", "engine")),
        })
    return result


def export_payload(rows: Iterable[DataRow], project: dict[str, Any] | None = None) -> dict[str, Any]:
    """Create a stable export contract for Excel, Power BI and APIs."""
    data = [asdict(row) for row in rows]
    return {
        "schema_version": "1.0",
        "project": project or {"name": "VvE Navigator"},
        "columns": ["entity", "year", "category", "value", "unit", "source"],
        "rows": data,
        "row_count": len(data),
    }
