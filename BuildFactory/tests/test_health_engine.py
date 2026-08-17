import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from health_engine import enterprise_health, summarize_health, HealthCheck


def test_healthy_summary():
    result = summarize_health([
        HealthCheck("a", "HEALTHY", 100, "ok"),
        HealthCheck("b", "HEALTHY", 100, "ok"),
    ])
    assert result["status"] == "HEALTHY"
    assert result["health_score"] == 100.0


def test_degraded_and_critical():
    degraded = summarize_health([HealthCheck("a", "DEGRADED", 70, "warn")])
    assert degraded["status"] == "DEGRADED"
    critical = summarize_health([HealthCheck("a", "DOWN", 0, "down")])
    assert critical["status"] == "CRITICAL"


def test_enterprise_health():
    result = enterprise_health({
        "enterprise_version": "2.2.0",
        "status": "READY",
        "release": {"quality_gate": {"can_publish": True, "blocking_count": 0, "issue_count": 0}},
        "manifest": {"fingerprint": "abc123"},
    })
    assert result["status"] == "HEALTHY"
    assert result["enterprise_status"] == "READY"
