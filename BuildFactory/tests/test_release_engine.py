import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from release_engine import run_release


def test_release_pipeline_sample_dataset():
    dataset = Path(__file__).parents[1] / "data" / "sample_vve_34.json"
    result = run_release(str(dataset), horizon_years=10)
    assert result["release_version"] == "1.9.0"
    assert "dashboard" in result
    assert "quality_gate" in result
    assert "datahub" in result
    assert isinstance(result["publishable"], bool)
