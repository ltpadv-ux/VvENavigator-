"""Enterprise core for VvE Navigator 2.3.0."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from release_engine import run_release
from release_manifest import create_manifest
from health_engine import enterprise_health
from policy_engine import PolicyProfile, load_policy, policy_snapshot


ENTERPRISE_VERSION = "2.3.0"


@dataclass(frozen=True)
class ReleaseProfile:
    name: str = "production"
    require_quality_gate: bool = True
    require_publishable: bool = True
    horizon_years: int = 30


def _effective_profile(
    profile: ReleaseProfile,
    policy: PolicyProfile | None,
) -> ReleaseProfile:
    if policy is None:
        return profile
    return ReleaseProfile(
        name=f"{profile.name}:{policy.name}",
        require_quality_gate=policy.require_quality_gate,
        require_publishable=policy.require_publishable,
        horizon_years=policy.horizon_years,
    )


def run_enterprise(
    dataset_path: str,
    profile: ReleaseProfile | None = None,
    policy_path: str | None = None,
) -> dict[str, Any]:
    """Execute the complete Navigator release using optional VvE policy controls."""
    profile = profile or ReleaseProfile()
    policy: PolicyProfile | None = None
    if policy_path:
        try:
            policy = load_policy(policy_path)
        except Exception as exc:
            result = {
                "enterprise_version": ENTERPRISE_VERSION,
                "release_profile": asdict(profile),
                "policy": {},
                "status": "ERROR",
                "reason": f"Policy profile ongeldig: {exc}",
                "release": {},
                "manifest": {},
            }
            result["health"] = enterprise_health(result)
            return result

    effective = _effective_profile(profile, policy)
    dataset = Path(dataset_path)
    if not dataset.exists():
        result = {
            "enterprise_version": ENTERPRISE_VERSION,
            "release_profile": asdict(effective),
            "policy": policy_snapshot(policy) if policy else {},
            "status": "ERROR",
            "reason": f"Dataset niet gevonden: {dataset_path}",
            "release": {},
            "manifest": {},
        }
        result["health"] = enterprise_health(result)
        return result

    try:
        release = run_release(str(dataset), horizon_years=effective.horizon_years)
    except Exception as exc:
        result = {
            "enterprise_version": ENTERPRISE_VERSION,
            "release_profile": asdict(effective),
            "policy": policy_snapshot(policy) if policy else {},
            "status": "ERROR",
            "reason": f"Release-run mislukt: {exc}",
            "release": {},
            "manifest": {},
        }
        result["health"] = enterprise_health(result)
        return result

    quality = release.get("quality_gate", {})
    can_publish = bool(quality.get("can_publish", False))

    if effective.require_quality_gate and not quality:
        status = "BLOCKED"
        reason = "Quality gate ontbreekt"
    elif effective.require_publishable and not can_publish:
        status = "BLOCKED"
        reason = "Quality gate blokkeert publicatie"
    else:
        status = "READY"
        reason = "Enterprise release voldoet aan release- en beleidsprofiel"

    manifest = create_manifest(
        ENTERPRISE_VERSION,
        effective.name,
        status,
        can_publish,
        dataset.name,
        effective.horizon_years,
        release,
    )

    result = {
        "enterprise_version": ENTERPRISE_VERSION,
        "release_profile": asdict(effective),
        "policy": policy_snapshot(policy) if policy else {},
        "status": status,
        "reason": reason,
        "release": release,
        "manifest": manifest,
    }
    result["health"] = enterprise_health(result)
    return result
