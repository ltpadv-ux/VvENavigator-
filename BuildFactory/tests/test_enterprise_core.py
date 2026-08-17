import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from enterprise_core import ENTERPRISE_VERSION, ReleaseProfile, run_enterprise


def test_enterprise_release_smoke():
    result = run_enterprise(str(ROOT / "data" / "sample_vve_34.json"), ReleaseProfile(horizon_years=5))
    assert result["enterprise_version"] == ENTERPRISE_VERSION == "2.0.0"
    assert result["status"] in {"READY", "BLOCKED"}
    assert result["release_profile"]["horizon_years"] == 5
    assert "release" in result
