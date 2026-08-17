"""Configuration and policy profiles for VvE Navigator Enterprise."""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PolicyProfile:
    name: str
    inflation_rate: float = 0.04
    discount_rate: float = 0.03
    horizon_years: int = 30
    reserve_floor: float = 0.0
    risk_critical: float = 75.0
    risk_high: float = 50.0
    risk_normal: float = 25.0
    require_quality_gate: bool = True
    require_publishable: bool = True
    scenario_set: str = "Basis-Duurzaam-Versneld"

    def validate(self) -> None:
        if self.inflation_rate <= -1:
            raise ValueError("inflation_rate must be greater than -1")
        if self.discount_rate <= -1:
            raise ValueError("discount_rate must be greater than -1")
        if self.horizon_years < 1:
            raise ValueError("horizon_years must be at least 1")
        if self.reserve_floor < 0:
            raise ValueError("reserve_floor must be non-negative")
        thresholds = [self.risk_critical, self.risk_high, self.risk_normal]
        if any(value < 0 or value > 100 for value in thresholds):
            raise ValueError("risk thresholds must be between 0 and 100")
        if not self.risk_critical >= self.risk_high >= self.risk_normal:
            raise ValueError("risk thresholds must be descending")


def profile_from_dict(data: dict[str, Any]) -> PolicyProfile:
    profile = PolicyProfile(
        name=str(data.get("name", "default")),
        inflation_rate=float(data.get("inflation_rate", 0.04)),
        discount_rate=float(data.get("discount_rate", 0.03)),
        horizon_years=int(data.get("horizon_years", 30)),
        reserve_floor=float(data.get("reserve_floor", 0.0)),
        risk_critical=float(data.get("risk_critical", 75.0)),
        risk_high=float(data.get("risk_high", 50.0)),
        risk_normal=float(data.get("risk_normal", 25.0)),
        require_quality_gate=bool(data.get("require_quality_gate", True)),
        require_publishable=bool(data.get("require_publishable", True)),
        scenario_set=str(data.get("scenario_set", "Basis-Duurzaam-Versneld")),
    )
    profile.validate()
    return profile


def load_policy(path: str | Path) -> PolicyProfile:
    policy_path = Path(path)
    if not policy_path.exists():
        raise FileNotFoundError(f"Policy profile not found: {policy_path}")
    payload = json.loads(policy_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Policy profile must be a JSON object")
    return profile_from_dict(payload)


def policy_snapshot(profile: PolicyProfile) -> dict[str, Any]:
    profile.validate()
    return asdict(profile)
