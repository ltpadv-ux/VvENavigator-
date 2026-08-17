import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from excel_master import Apartment
from mjop_engine import MJOPComponent
from navigator_mvp import build_mvp


def test_integrated_mvp():
    result = build_mvp(
        [Apartment("01"), Apartment("02")],
        [MJOPComponent("Schilderwerk", "Gevel", 100, "m2", 40, 6, 2025, 3, 20, 10, 5)],
        2026,
        100000,
        horizon_years=5,
    )
    assert "dashboard" in result
    assert "workbook" in result
    assert "datahub" in result
    assert result["alv_report"]["planning_horizon_years"] == 5
    assert result["workbook"]["vve"]["apartments"] == 2
