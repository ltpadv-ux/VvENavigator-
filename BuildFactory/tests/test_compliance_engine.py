import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from compliance_engine import quality_gate, validate_mjop_row


def test_invalid_mjop_row_blocks():
    issues = validate_mjop_row({"year": 2030, "component": "Dak", "bouwdeel": "Dak", "indexed_cost": -1, "condition_score": 7})
    assert any(i.code == "NEGATIVE_COST" for i in issues)
    assert any(i.code == "INVALID_CONDITION" for i in issues)


def test_quality_gate_blocks_negative_reserve():
    result = quality_gate(
        [{"year": 2030, "component": "Dak", "bouwdeel": "Dak", "indexed_cost": 1000, "condition_score": 3}],
        [{"year": 2030, "reserve_closing": -100}],
        [{"action": "Dak uitvoeren", "priority": "NU", "rationale": "Risico", "horizon": "0-1 jaar"}],
    )
    assert result["status"] == "BLOKKEREN"
    assert result["can_publish"] is False


def test_quality_gate_approves_clean_data():
    result = quality_gate(
        [{"year": 2030, "component": "Dak", "bouwdeel": "Dak", "indexed_cost": 1000, "condition_score": 3}],
        [{"year": 2030, "reserve_closing": 10000}],
        [{"action": "Dak plannen", "priority": "PLANNEN", "rationale": "Conditie", "horizon": "2-5 jaar"}],
    )
    assert result["status"] == "GOEDGEKEURD"
    assert result["can_publish"] is True
