"""Audit & Control Engine for VvE Navigator."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Iterable


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    entity: str
    action: str
    actor: str
    reason: str
    before: str = ""
    after: str = ""
    timestamp: str = ""

    def normalized(self) -> dict:
        data = asdict(self)
        if not data["timestamp"]:
            data["timestamp"] = datetime.now(timezone.utc).isoformat()
        return data


def record_event(
    event_type: str,
    entity: str,
    action: str,
    actor: str,
    reason: str,
    before: str = "",
    after: str = "",
    timestamp: str = "",
) -> dict:
    if not event_type or not entity or not action or not actor or not reason:
        raise ValueError("event_type, entity, action, actor and reason are required")
    return AuditEvent(event_type, entity, action, actor, reason, before, after, timestamp).normalized()


def budget_change(entity: str, actor: str, reason: str, before: float, after: float, timestamp: str = "") -> dict:
    event = record_event(
        "BUDGET_MUTATION",
        entity,
        "budget gewijzigd",
        actor,
        reason,
        f"{before:.2f}",
        f"{after:.2f}",
        timestamp,
    )
    event["delta"] = round(after - before, 2)
    return event


def audit_summary(events: Iterable[dict]) -> dict:
    rows = list(events)
    by_type: dict[str, int] = {}
    actors: set[str] = set()
    for row in rows:
        event_type = str(row.get("event_type", "UNKNOWN"))
        by_type[event_type] = by_type.get(event_type, 0) + 1
        actor = str(row.get("actor", "")).strip()
        if actor:
            actors.add(actor)
    return {
        "events": len(rows),
        "event_types": dict(sorted(by_type.items())),
        "actors": sorted(actors),
        "complete_trace": all(
            bool(row.get("actor")) and bool(row.get("reason")) and bool(row.get("timestamp"))
            for row in rows
        ),
    }
