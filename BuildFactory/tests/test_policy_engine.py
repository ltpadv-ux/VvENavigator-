import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from policy_engine import PolicyProfile, load_policy, profile_from_dict


def test_policy_defaults_and_validation():
    profile = PolicyProfile(name="test")
    profile.validate()
    assert profile.horizon_years == 30
    assert profile.risk_critical == 75.0


def test_policy_rejects_invalid_thresholds():
    with pytest.raises(ValueError):
        profile_from_dict({"name": "bad", "risk_critical": 40, "risk_high": 60, "risk_normal": 20})


def test_load_policy(tmp_path):
    path = tmp_path / "policy.json"
    path.write_text(json.dumps({"name": "custom", "reserve_floor": 75000, "horizon_years": 25}), encoding="utf-8")
    profile = load_policy(path)
    assert profile.name == "custom"
    assert profile.reserve_floor == 75000
    assert profile.horizon_years == 25
