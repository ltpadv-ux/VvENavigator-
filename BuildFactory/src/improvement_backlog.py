"""Continuous improvement backlog for VvE Navigator reliability work."""
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

BACKLOG_VERSION = "4.8.0"
DEFAULT_OWNER = {
    "Compliance & Quality": "Bestuur / Beheerder",
    "Rendering": "Technisch beheer",
    "Packaging": "Technisch beheer",
    "Release Validation": "Release verantwoordelijke",
    "Release Control": "Release verantwoordelijke",
    "Overig": "Product owner",
}


def _item_id(category: str, check: str) -> str:
    raw = f"{category}-{check}".lower().replace(" ", "-").replace("&", "en")
    return "IMP-" + "".join(c for c in raw if c.isalnum() or c == "-")[:48]


def build_improvement_backlog(improvement: dict[str, Any], existing: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    existing = existing or []
    by_id = {str(x.get("id")): dict(x) for x in existing if x.get("id")}
    now = datetime.now(timezone.utc).isoformat()
    for cause in improvement.get("root_causes", []) or []:
        category = str(cause.get("category", "Overig")); check = str(cause.get("check", "unknown")); item_id = _item_id(category, check)
        previous = by_id.get(item_id, {})
        occurrences = int(cause.get("occurrences", 0) or 0)
        impact = int(cause.get("impact_score", 0) or 0)
        priority = str(cause.get("priority", "LAAG"))
        by_id[item_id] = {
            "id": item_id,
            "title": f"Structurele verbetering: {category}",
            "category": category,
            "check": check,
            "owner": previous.get("owner", DEFAULT_OWNER.get(category, DEFAULT_OWNER["Overig"])),
            "status": previous.get("status", "OPEN"),
            "priority": priority,
            "impact_score": impact,
            "occurrences": occurrences,
            "progress_percent": int(previous.get("progress_percent", 0) or 0),
            "recommended_action": str(cause.get("recommended_action", "Onderzoek en herstel de structurele oorzaak.")),
            "created_at": previous.get("created_at", now),
            "updated_at": now,
        }
    order = {"HOOG": 0, "MIDDEL": 1, "LAAG": 2, "GEEN": 3}
    items = sorted(by_id.values(), key=lambda x: (order.get(str(x.get("priority")), 9), -int(x.get("impact_score", 0) or 0), str(x.get("id", ""))))
    open_items = [x for x in items if str(x.get("status", "OPEN")).upper() not in {"GEREED", "DONE", "CLOSED"}]
    return {
        "continuous_improvement_backlog_version": BACKLOG_VERSION,
        "status": "ACTIE VEREIST" if open_items else "BIJGEWERKT",
        "item_count": len(items),
        "open_count": len(open_items),
        "high_priority_open": sum(1 for x in open_items if x.get("priority") == "HOOG"),
        "items": items,
        "next_action": open_items[0].get("recommended_action", "Geen open verbeteractie") if open_items else "Geen open verbeteractie",
    }


def update_backlog_file(path: str | Path, improvement: dict[str, Any]) -> dict[str, Any]:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True); existing: list[dict[str, Any]] = []
    if p.exists():
        try: existing = (json.loads(p.read_text(encoding="utf-8")) or {}).get("items", [])
        except Exception: existing = []
    backlog = build_improvement_backlog(improvement, existing)
    p.write_text(json.dumps(backlog, ensure_ascii=False, indent=2), encoding="utf-8")
    return backlog
