"""Action & execution engine for approved VvE decisions."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date
from typing import Iterable


@dataclass(frozen=True)
class ActionItem:
    title: str
    owner: str
    deadline: str
    budget: float
    spent: float = 0.0
    progress_pct: float = 0.0
    status: str = "OPEN"

    @property
    def budget_variance(self) -> float:
        return round(self.budget - self.spent, 2)

    @property
    def traffic_light(self) -> str:
        if self.status.upper() in {"BLOKKADE", "GESTOPT"}:
            return "ROOD"
        if self.spent > self.budget:
            return "ROOD"
        if self.progress_pct < 50 and self.status.upper() == "VERTRAAGD":
            return "ORANJE"
        if self.progress_pct >= 100 or self.status.upper() == "GEREED":
            return "GROEN"
        return "GEEL"


def build_action(
    title: str,
    owner: str,
    deadline: str,
    budget: float,
    spent: float = 0.0,
    progress_pct: float = 0.0,
    status: str = "OPEN",
) -> dict:
    if budget < 0 or spent < 0:
        raise ValueError("budget and spent must be non-negative")
    if not 0 <= progress_pct <= 100:
        raise ValueError("progress_pct must be between 0 and 100")
    item = ActionItem(title, owner, deadline, budget, spent, progress_pct, status)
    row = asdict(item)
    row["budget_variance"] = item.budget_variance
    row["traffic_light"] = item.traffic_light
    return row


def execution_summary(actions: Iterable[dict]) -> dict:
    rows = list(actions)
    total_budget = sum(float(a.get("budget", 0.0)) for a in rows)
    total_spent = sum(float(a.get("spent", 0.0)) for a in rows)
    lights = {"GROEN": 0, "GEEL": 0, "ORANJE": 0, "ROOD": 0}
    for action in rows:
        light = str(action.get("traffic_light", "GEEL"))
        if light in lights:
            lights[light] += 1
    return {
        "actions": len(rows),
        "total_budget": round(total_budget, 2),
        "total_spent": round(total_spent, 2),
        "budget_variance": round(total_budget - total_spent, 2),
        "traffic_lights": lights,
    }
