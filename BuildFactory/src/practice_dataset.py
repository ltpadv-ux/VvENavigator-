"""Load and validate the bundled 34-apartment VvE practice dataset."""
from __future__ import annotations

import json
from pathlib import Path

from excel_master import Apartment
from mjop_engine import MJOPComponent

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = ROOT / "data" / "sample_vve_34.json"


def load_practice_dataset(path: Path | None = None) -> dict:
    source = path or DEFAULT_DATASET
    payload = json.loads(source.read_text(encoding="utf-8"))
    vve = payload["vve"]
    if int(vve["apartments"]) != 34:
        raise ValueError("practice dataset must contain 34 apartments")
    if float(vve["reserve_fund"]) < 0:
        raise ValueError("reserve_fund must be non-negative")
    return payload


def to_domain_objects(payload: dict) -> tuple[list[Apartment], list[MJOPComponent]]:
    apartments = [Apartment(f"{index:02d}") for index in range(1, int(payload["vve"]["apartments"]) + 1)]
    components = [MJOPComponent(**row) for row in payload["components"]]
    return apartments, components
