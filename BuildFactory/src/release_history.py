"""Release history and trend monitoring for VvE Navigator."""
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

HISTORY_VERSION = "4.5.0"


def summarize_run(report: dict[str, Any]) -> dict[str, Any]:
    control = report.get("control_center", {}) or {}
    diagnostics = report.get("diagnostics", {}) or {}
    healing = report.get("self_healing", {}) or {}
    quality = report.get("release", {}).get("enterprise", {}).get("release", {}).get("quality_gate", {}) or {}
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "control_status": control.get("status", "ONBEKEND"),
        "verification_status": (report.get("verification", {}) or {}).get("status", ""),
        "self_healing_status": healing.get("status", "NOT_RUN"),
        "repair_count": len(healing.get("repairs", []) or []),
        "blocker_count": diagnostics.get("blocker_count", 0),
        "quality_issue_count": len(quality.get("issues", []) or []),
    }


def append_history(history_file: str | Path, report: dict[str, Any], keep_last: int = 100) -> dict[str, Any]:
    path = Path(history_file); path.parent.mkdir(parents=True, exist_ok=True)
    history: list[dict[str, Any]] = []
    if path.exists():
        try:
            history = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            history = []
    history.append(summarize_run(report)); history = history[-max(1, keep_last):]
    path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    return build_trend_monitor(history)


def build_trend_monitor(history: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(history)
    green = sum(1 for x in history if x.get("control_status") == "GROEN")
    healed = sum(1 for x in history if x.get("control_status") == "HERSTELD")
    blocked = sum(1 for x in history if x.get("control_status") == "GEBLOKKEERD")
    reliability = round(((green + 0.75 * healed) / total * 100), 1) if total else 0.0
    recent = history[-10:]
    recent_blocked = sum(1 for x in recent if x.get("control_status") == "GEBLOKKEERD")
    trend = "STABIEL"
    if total >= 2:
        prior = history[:-1][-10:]
        prior_blocked = sum(1 for x in prior if x.get("control_status") == "GEBLOKKEERD")
        trend = "VERSLECHTEREND" if recent_blocked > prior_blocked else "VERBETEREND" if recent_blocked < prior_blocked else "STABIEL"
    return {
        "release_history_version": HISTORY_VERSION,
        "runs": total,
        "green_runs": green,
        "healed_runs": healed,
        "blocked_runs": blocked,
        "total_repairs": sum(int(x.get("repair_count", 0)) for x in history),
        "total_quality_issues": sum(int(x.get("quality_issue_count", 0)) for x in history),
        "release_reliability_score": reliability,
        "trend": trend,
        "latest": history[-1] if history else {},
    }
