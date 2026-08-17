import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from navigator_mvp import build_mvp
from practice_dataset import load_practice_dataset, to_domain_objects


def test_practice_dataset_end_to_end():
    payload = load_practice_dataset()
    apartments, components = to_domain_objects(payload)
    result = build_mvp(
        apartments,
        components,
        payload["vve"]["base_year"],
        payload["vve"]["reserve_fund"],
        horizon_years=30,
    )
    assert len(apartments) == 34
    assert len(components) >= 8
    assert result["workbook"]["vve"]["apartments"] == 34
    assert result["datahub"]["row_count"] > 0
    assert result["alv_report"]["planning_horizon_years"] == 30
