"""Reliability KPI and SLA monitoring for VvE Navigator."""
from __future__ import annotations
from typing import Any

SLA_VERSION = "4.6.0"


def evaluate_reliability_sla(
    trend_monitor: dict[str, Any],
    minimum_reliability: float = 95.0,
    max_blocked_recent: int = 1,
) -> dict[str, Any]:
    score = float(trend_monitor.get("release_reliability_score", 0.0) or 0.0)
    runs = int(trend_monitor.get("runs", 0) or 0)
    blocked = int(trend_monitor.get("blocked_runs", 0) or 0)
    trend = str(trend_monitor.get("trend", "STABIEL"))
    issues: list[str] = []

    reliability_ok = score >= minimum_reliability
    if not reliability_ok:
        issues.append(f"Release reliability {score:.1f}% ligt onder SLA-norm {minimum_reliability:.1f}%")

    blocked_ok = blocked <= max_blocked_recent if runs <= 10 else True
    if not blocked_ok:
        issues.append(f"Te veel geblokkeerde runs: {blocked} > {max_blocked_recent}")

    trend_ok = trend != "VERSLECHTEREND"
    if not trend_ok:
        issues.append("Releasekwaliteit vertoont een verslechterende trend")

    compliant = reliability_ok and blocked_ok and trend_ok
    return {
        "reliability_sla_version": SLA_VERSION,
        "status": "BINNEN SLA" if compliant else "SLA BREACH",
        "compliant": compliant,
        "minimum_reliability": minimum_reliability,
        "release_reliability_score": score,
        "trend": trend,
        "runs": runs,
        "blocked_runs": blocked,
        "checks": {
            "reliability": reliability_ok,
            "blocked_runs": blocked_ok,
            "trend": trend_ok,
        },
        "issues": issues,
        "next_action": "Geen actie nodig" if compliant else "Analyseer de releasehistorie en herstel de dominante oorzaak van de SLA-afwijking.",
    }
