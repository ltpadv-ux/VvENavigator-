import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from release_manifest import build_fingerprint, create_manifest


def test_fingerprint_is_stable():
    payload = {"b": 2, "a": 1}
    assert build_fingerprint(payload) == build_fingerprint({"a": 1, "b": 2})


def test_manifest_contains_release_controls():
    release = {"project": "Demo", "dashboard": {"vni": 80}, "annual_mjop_totals": {2027: 1000}, "quality_gate": {"can_publish": True}}
    manifest = create_manifest("2.1.0", "production", "READY", True, "sample.json", 30, release)
    assert manifest["version"] == "2.1.0"
    assert manifest["status"] == "READY"
    assert len(manifest["fingerprint"]) == 64
