"""Board and ALV reporting engine for the VvE Navigator."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ReportMetric:
    name: str
    value: float
    unit: str = ""
    status: str = ""


def status_label(score: float) -> str:
    if score >= 75:
        return "KRITIEK"
    if score >= 50:
        return "HOOG"
    if score >= 25:
        return "NORMAAL"
    return "LAAG"


def build_board_summary(vni: float, mgi: float, reserve: float, liquidity: float, risk_score: float, top_actions: Iterable[str]) -> dict:
    metrics = [
        ReportMetric("VNI", round(vni, 2), "/100", status_label(100 - vni)),
        ReportMetric("MGI", round(mgi, 2), "/100", status_label(100 - mgi)),
        ReportMetric("Reservefonds", round(reserve, 2), "EUR"),
        ReportMetric("Liquiditeit", round(liquidity, 2), "EUR", "OK" if liquidity >= 0 else "TEKORT"),
        ReportMetric("Risicoscore", round(risk_score, 2), "/100", status_label(risk_score)),
    ]
    return {
        "metrics": [metric.__dict__ for metric in metrics],
        "top_actions": list(top_actions)[:3],
        "decision_focus": "Stuur op risico, onderhoud en financiële weerbaarheid.",
    }


def build_alv_report(summary: dict, planning_years: int = 30) -> dict:
    if planning_years <= 0:
        raise ValueError("planning_years must be positive")
    return {
        "title": "VvE Navigator — ALV Rapport",
        "planning_horizon_years": planning_years,
        "management_summary": summary.get("decision_focus", ""),
        "metrics": summary.get("metrics", []),
        "top_decisions": summary.get("top_actions", []),
    }
