"""Observability and health scoring for VvE Navigator Enterprise."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Iterable


@dataclass(frozen=True)
class HealthCheck:
    name: str
    status: str
    score: float
    message: str


def check_release(release: dict[str, Any]) -> HealthCheck:
    quality = release.get("quality_gate", {})
    if not release:
        return HealthCheck("release", "DOWN", 0.0, "Release ontbreekt")
    if quality and not quality.get("can_publish", False):
        return HealthCheck("release", "DEGRADED", 50.0, "Release aanwezig maar quality gate blokkeert")
    return HealthCheck("release", "HEALTHY", 100.0, "Release beschikbaar en publiceerbaar")


def check_manifest(manifest: dict[str, Any]) -> HealthCheck:
    fingerprint = manifest.get("fingerprint") or manifest.get("regression_fingerprint")
    if not manifest:
        return HealthCheck("manifest", "DOWN", 0.0, "Release manifest ontbreekt")
    if not fingerprint:
        return HealthCheck("manifest", "DEGRADED", 60.0, "Manifest aanwezig zonder regressie-fingerprint")
    return HealthCheck("manifest", "HEALTHY", 100.0, "Manifest en regressie-fingerprint aanwezig")


def check_quality(release: dict[str, Any]) -> HealthCheck:
    quality = release.get("quality_gate", {})
    if not quality:
        return HealthCheck("quality_gate", "DOWN", 0.0, "Quality gate ontbreekt")
    blocking = int(quality.get("blocking_count", 0))
    issues = int(quality.get("issue_count", 0))
    if blocking > 0:
        return HealthCheck("quality_gate", "DOWN", 20.0, f"{blocking} blokkerende kwaliteitsissues")
    if issues > 0:
        return HealthCheck("quality_gate", "DEGRADED", 80.0, f"{issues} niet-blokkerende kwaliteitsissues")
    return HealthCheck("quality_gate", "HEALTHY", 100.0, "Geen kwaliteitsissues")


def summarize_health(checks: Iterable[HealthCheck]) -> dict[str, Any]:
    rows = list(checks)
    score = round(sum(item.score for item in rows) / len(rows), 1) if rows else 0.0
    if any(item.status == "DOWN" for item in rows):
        status = "CRITICAL"
    elif any(item.status == "DEGRADED" for item in rows):
        status = "DEGRADED"
    else:
        status = "HEALTHY"
    return {
        "status": status,
        "health_score": score,
        "checks": [asdict(item) for item in rows],
        "warnings": [item.message for item in rows if item.status != "HEALTHY"],
    }


def enterprise_health(enterprise_result: dict[str, Any]) -> dict[str, Any]:
    """Create a health dashboard from an Enterprise run result."""
    release = enterprise_result.get("release", {})
    manifest = enterprise_result.get("manifest", {})
    checks = [check_release(release), check_manifest(manifest), check_quality(release)]
    summary = summarize_health(checks)
    summary["enterprise_status"] = enterprise_result.get("status", "UNKNOWN")
    summary["enterprise_version"] = enterprise_result.get("enterprise_version", "unknown")
    return summary
