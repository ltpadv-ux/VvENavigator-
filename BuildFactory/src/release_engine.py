"""Integration and release orchestration for the VvE Navigator."""
from __future__ import annotations

from typing import Any

from compliance_engine import quality_gate
from navigator_mvp import build_mvp
from practice_dataset import load_practice_dataset


def run_release(dataset_path: str, horizon_years: int = 30) -> dict[str, Any]:
    """Run the practice dataset through the integrated Navigator release pipeline."""
    practice = load_practice_dataset(dataset_path)
    mvp = build_mvp(
        practice["apartments"],
        practice["components"],
        practice["base_year"],
        practice["reserve_fund"],
        horizon_years=horizon_years,
        inflation_rate=practice.get("inflation_rate", 0.04),
    )

    # The dashboard currently exposes short action labels, not full Decision
    # records. Only structured decisions should enter the compliance validator.
    structured_decisions: list[dict[str, Any]] = []

    quality = quality_gate(
        mjop_rows=mvp.get("mjop", []),
        reserve_rows=[
            {
                "year": practice["base_year"],
                "reserve_closing": practice["reserve_fund"],
            }
        ],
        decisions=structured_decisions,
    )

    return {
        "release_version": "1.9.0",
        "project": practice.get("name", "VvE Navigator Practice Release"),
        "quality_gate": quality,
        "publishable": bool(quality.get("can_publish", False)),
        "dashboard": mvp.get("dashboard", {}),
        "alv_report": mvp.get("alv_report", {}),
        "mjop": mvp.get("mjop", []),
        "annual_mjop_totals": mvp.get("annual_mjop_totals", {}),
        "workbook": mvp.get("workbook", {}),
        "datahub": mvp.get("datahub", {}),
    }
