import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from excel_master import Apartment, MaintenanceItem, annual_mjop_totals, build_workbook_model


def test_workbook_model():
    apartments = [Apartment("01"), Apartment("02")]
    items = [
        MaintenanceItem("Gevel", "Schilderwerk", 2028, 10000),
        MaintenanceItem("Gevel", "Schilderwerk", 2028, 5000),
    ]
    model = build_workbook_model(apartments, items, 223772.26)
    assert model["vve"]["apartments"] == 2
    assert model["vve"]["reserve_fund"] == 223772.26
    assert len(model["sheets"]) == 9


def test_annual_totals():
    items = [
        MaintenanceItem("Dak", "Onderhoud", 2030, 12000),
        MaintenanceItem("Dak", "Onderhoud", 2030, 3000),
        MaintenanceItem("Lift", "Onderhoud", 2031, 5000),
    ]
    assert annual_mjop_totals(items) == {2030: 15000, 2031: 5000}
