"""Compliance and quality controls for VvE Navigator outputs."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable, Any


@dataclass(frozen=True)
class QualityIssue:
    code: str
    severity: str
    message: str
    field: str = ""
    blocking: bool = False


def validate_mjop_row(row: dict[str, Any]) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    required = ("year", "component", "bouwdeel", "indexed_cost", "condition_score")
    for key in required:
        if key not in row or row.get(key) in (None, ""):
            issues.append(QualityIssue("MISSING_FIELD", "HOOG", f"Ontbrekend veld: {key}", key, True))
    if "indexed_cost" in row and float(row.get("indexed_cost", 0)) < 0:
        issues.append(QualityIssue("NEGATIVE_COST", "KRITIEK", "MJOP-kosten mogen niet negatief zijn", "indexed_cost", True))
    if "condition_score" in row:
        try:
            score = int(row["condition_score"])
            if not 1 <= score <= 6:
                issues.append(QualityIssue("INVALID_CONDITION", "HOOG", "Conditiescore moet tussen 1 en 6 liggen", "condition_score", True))
        except (TypeError, ValueError):
            issues.append(QualityIssue("INVALID_CONDITION", "HOOG", "Conditiescore is ongeldig", "condition_score", True))
    return issues


def validate_financials(reserve_rows: Iterable[dict[str, Any]]) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    for row in reserve_rows:
        year = row.get("year", "?")
        closing = float(row.get("reserve_closing", row.get("closing_reserve", 0.0)))
        if closing < 0:
            issues.append(QualityIssue("NEGATIVE_RESERVE", "KRITIEK", f"Negatief reservefonds in {year}", "reserve_closing", True))
    return issues


def validate_decisions(decisions: Iterable[dict[str, Any]]) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    for index, item in enumerate(decisions, start=1):
        for key in ("action", "priority", "rationale", "horizon"):
            if not item.get(key):
                issues.append(QualityIssue("INCOMPLETE_DECISION", "HOOG", f"Besluit {index} mist {key}", key, True))
    return issues


def quality_gate(
    mjop_rows: Iterable[dict[str, Any]],
    reserve_rows: Iterable[dict[str, Any]],
    decisions: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    issues: list[QualityIssue] = []
    for row in mjop_rows:
        issues.extend(validate_mjop_row(row))
    issues.extend(validate_financials(reserve_rows))
    issues.extend(validate_decisions(decisions))
    blocking = [issue for issue in issues if issue.blocking]
    return {
        "status": "BLOKKEREN" if blocking else "GOEDGEKEURD",
        "can_publish": not blocking,
        "issue_count": len(issues),
        "blocking_count": len(blocking),
        "issues": [asdict(issue) for issue in issues],
    }
