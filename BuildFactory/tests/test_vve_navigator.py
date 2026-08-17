import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from vve_navigator import MaintenanceItem, maintenance_priority, net_present_value


def test_indexed_cost():
    item = MaintenanceItem("Gevel", 2028, 10000)
    assert round(item.indexed_cost(0.04, 2026), 2) == 10816.00


def test_npv():
    assert round(net_present_value([1000, -500, -500], 0.10), 2) == 132.23


def test_priority():
    assert maintenance_priority(80, 60, 50) == 69.0
