"""Release manifest and regression fingerprinting for VvE Navigator Enterprise."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
from json import dumps
from typing import Any


@dataclass(frozen=True)
class ReleaseManifest:
    version: str
    profile: str
    status: str
    publishable: bool
    dataset: str
    horizon_years: int
    fingerprint: str


def build_fingerprint(payload: dict[str, Any]) -> str:
    canonical = dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(canonical.encode("utf-8")).hexdigest()


def create_manifest(
    version: str,
    profile: str,
    status: str,
    publishable: bool,
    dataset: str,
    horizon_years: int,
    release_payload: dict[str, Any],
) -> dict[str, Any]:
    fingerprint_payload = {
        "dashboard": release_payload.get("dashboard", {}),
        "annual_mjop_totals": release_payload.get("annual_mjop_totals", {}),
        "quality_gate": release_payload.get("quality_gate", {}),
        "project": release_payload.get("project", ""),
    }
    manifest = ReleaseManifest(
        version=version,
        profile=profile,
        status=status,
        publishable=publishable,
        dataset=dataset,
        horizon_years=horizon_years,
        fingerprint=build_fingerprint(fingerprint_payload),
    )
    return asdict(manifest)
