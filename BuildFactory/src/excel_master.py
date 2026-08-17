"""Excel Master Workbook data model for VvE Navigator."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable


@dataclass(frozen=True)
class Apartment:
    number: str
    ownership_share: float = 1.0


@dataclass(frozen=True)
class MaintenanceItem:
    building_part: str
    component: str
    year: int
    amount: float
    condition: int = 3
    priority: int = 3


def build_workbook_model(
    apartments: Iterable[Apartment],
    maintenance: Iterable[MaintenanceItem],
    reserve_fund: float = 0.0,
) -> dict:
    """Create a spreadsheet-neutral master workbook model."""
    apartments = list(apartments)
    maintenance = list(maintenance)
    return {
        "sheets": [
            "Dashboard", "VvE", "Appartementen", "MJOP", "Finance",
            "Risico", "Instellingen", "Rapportage", "Export"
        ],
        "vve": {
            "apartments": len(apartments),
            "reserve_fund": round(reserve_fund, 2),
        },
        "apartments": [asdict(item) for item in apartments],
        "mjop": [asdict(item) for item in maintenance],
    }


def annual_mjop_totals(items: Iterable[MaintenanceItem]) -> dict[int, float]:
    totals: dict[int, float] = {}
    for item in items:
        totals[item.year] = round(totals.get(item.year, 0.0) + item.amount, 2)
    return dict(sorted(totals.items()))
