"""Integrated VvE Navigator MVP orchestration layer."""
from __future__ import annotations

from typing import Any, Iterable

from datahub import DataRow, export_payload
from excel_master import Apartment, MaintenanceItem, annual_mjop_totals, build_workbook_model
from mjop_engine import MJOPComponent, generate_plan
from report_engine import build_alv_report, build_board_summary


def build_mvp(
    apartments: Iterable[Apartment],
    components: Iterable[MJOPComponent],
    start_year: int,
    reserve_fund: float,
    horizon_years: int = 30,
    inflation_rate: float = 0.04,
) -> dict[str, Any]:
    """Run the core engines and return one integrated MVP payload."""
    apartments = list(apartments)
    components = list(components)
    plan = generate_plan(components, start_year, horizon_years, inflation_rate)
    totals = {int(year): float(value) for year, value in annual_mjop_totals(
        MaintenanceItem(r["bouwdeel"], r["component"], r["year"], r["indexed_cost"], r["condition_score"], 3)
        for r in plan
    ).items()}

    first_year_spend = totals.get(start_year, 0.0)
    liquidity = reserve_fund - first_year_spend
    risk_score = max((float(c.risk_score) for c in components), default=0.0)
    condition = sum(c.condition_score for c in components) / len(components) if components else 3.0
    condition_score = max(0.0, min(100.0, (7.0 - condition) / 6.0 * 100.0))
    reserve_score = max(0.0, min(100.0, reserve_fund / max(first_year_spend, 1.0) * 100.0))
    mjop_score = max(0.0, 100.0 - min(100.0, first_year_spend / max(reserve_fund, 1.0) * 100.0))
    vni = round(0.35 * reserve_score + 0.25 * mjop_score + 0.25 * (100 - risk_score) + 0.15 * condition_score, 2)
    top_actions = []
    if liquidity < 0:
        top_actions.append("Reservefonds en VvE-bijdrage herijken")
    if risk_score >= 50:
        top_actions.append("Hoogste onderhoudsrisico's aanpakken")
    if first_year_spend > 0:
        top_actions.append("MJOP-uitgaven voor komende jaren vaststellen")
    top_actions = top_actions[:3]

    summary = build_board_summary(vni, mjop_score, reserve_fund, liquidity, risk_score, top_actions)
    rows = [DataRow("VvE", year, "MJOP", value) for year, value in totals.items()]
    return {
        "dashboard": summary,
        "alv_report": build_alv_report(summary, horizon_years),
        "mjop": plan,
        "annual_mjop_totals": totals,
        "workbook": build_workbook_model(apartments, [
            MaintenanceItem(r["bouwdeel"], r["component"], r["year"], r["indexed_cost"], r["condition_score"], 3)
            for r in plan
        ], reserve_fund),
        "datahub": export_payload(rows),
    }
