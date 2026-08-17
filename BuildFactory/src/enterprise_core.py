"""Enterprise core for VvE Navigator 2.0.0."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from release_engine import run_release


ENTERPRISE_VERSION = "2.0.0"


@dataclass(frozen=True)
class ReleaseProfile:
    name: str = "production"
    require_quality_gate: bool = True
    require_publishable: bool = True
    horizon_years: int = 30


def run_enterprise(dataset_path: str, profile: ReleaseProfile | None = None) -> dict[str, Any]:
    """Execute the complete Navigator release with enterprise release controls."""
    profile = profile or ReleaseProfile()
    release = run_release(dataset_path, horizon_years=profile.horizon_years)
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

    return {
        "enterprise_version": ENTERPRISE_VERSION,
        "release_profile": asdict(profile),
        "status": status,
        "reason": reason,
        "release": release,
    }
