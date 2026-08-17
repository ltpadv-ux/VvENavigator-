"""Enterprise core for VvE Navigator 2.2.0."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from release_engine import run_release
from release_manifest import create_manifest
from health_engine import enterprise_health


ENTERPRISE_VERSION = "2.2.0"


@dataclass(frozen=True)
class ReleaseProfile:
    name: str = "production"
    require_quality_gate: bool = True
    require_publishable: bool = True
    horizon_years: int = 30


def run_enterprise(dataset_path: str, profile: ReleaseProfile | None = None) -> dict[str, Any]:
    """Execute the complete Navigator release with hardened release controls."""
    profile = profile or ReleaseProfile()
    dataset = Path(dataset_path)
    if not dataset.exists():
        result = {
            "enterprise_version": ENTERPRISE_VERSION,
            "release_profile": asdict(profile),
            "status": "ERROR",
            "reason": f"Dataset niet gevonden: {dataset_path}",
            "release": {},
            "manifest": {},
        }
        result["health"] = enterprise_health(result)
        return result

    try:
        release = run_release(str(dataset), horizon_years=profile.horizon_years)
    except Exception as exc:
        result = {
            "enterprise_version": ENTERPRISE_VERSION,
            "release_profile": asdict(profile),
            "status": "ERROR",
            "reason": f"Release-run mislukt: {exc}",
            "release": {},
            "manifest": {},
        }
        result["health"] = enterprise_health(result)
        return result

    quality = release.get("quality_gate", {})
    can_publish = bool(quality.get("can_publish", False))

    if profile.require_quality_gate and not quality:
        status = "BLOCKED"
        reason = "Quality gate ontbreekt"
    elif profile.require_publishable and not can_publish:
        status = "BLOCKED"
        reason = "Quality gate blokkeert publicatie"
    else:
        status = "READY"
        reason = "Enterprise release voldoet aan releaseprofiel"

    manifest = create_manifest(
        ENTERPRISE_VERSION,
        profile.name,
        status,
        can_publish,
        dataset.name,
        profile.horizon_years,
        release,
    )

    result = {
        "enterprise_version": ENTERPRISE_VERSION,
        "release_profile": asdict(profile),
        "status": status,
        "reason": reason,
        "release": release,
        "manifest": manifest,
    }
    result["health"] = enterprise_health(result)
    return result
