import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from scenario_engine import Scenario, compare_scenarios


def test_compare_scenarios():
    base = {2027: 10000, 2028: 20000}
    results = compare_scenarios(base, [Scenario("Basis"), Scenario("Duurzaam", 1.1, .2, .25)], 25000)
    assert results[0]["total_mjop"] == 30000
    assert results[1]["energy_saving_pct"] == 20.0
    assert results[1]["co2_reduction_pct"] == 25.0
