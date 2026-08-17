import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from audit_engine import audit_summary, budget_change, record_event


def test_record_event_has_trace_fields():
    event = record_event(
        "DECISION",
        "Lift",
        "besluit vastgesteld",
        "Bestuur",
        "ALV akkoord",
        timestamp="2026-08-17T12:00:00+00:00",
    )
    assert event["actor"] == "Bestuur"
    assert event["reason"] == "ALV akkoord"
    assert event["timestamp"].startswith("2026-08-17")


def test_budget_change_delta():
    event = budget_change("Dak", "Penningmeester", "offerte bijgesteld", 10000, 12500, "2026-08-17T12:00:00+00:00")
    assert event["delta"] == 2500
    assert event["event_type"] == "BUDGET_MUTATION"


def test_audit_summary():
    events = [
        record_event("DECISION", "Dak", "goedgekeurd", "Bestuur", "ALV", timestamp="2026-08-17T12:00:00+00:00"),
        record_event("EXECUTION", "Dak", "gestart", "Beheerder", "opdracht verstrekt", timestamp="2026-08-18T12:00:00+00:00"),
    ]
    summary = audit_summary(events)
    assert summary["events"] == 2
    assert summary["complete_trace"] is True
    assert summary["actors"] == ["Beheerder", "Bestuur"]
