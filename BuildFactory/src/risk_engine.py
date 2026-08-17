"""Risk scoring engine for VvE Navigator maintenance decisions."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskAssessment:
    """Normalized risk assessment for a maintenance component."""

    component: str
    condition_score: int
    probability: float
    impact: float
    urgency: float = 0.0
    financial_impact: float = 0.0

    def __post_init__(self) -> None:
        if not 1 <= self.condition_score <= 6:
            raise ValueError("condition_score must be 1-6")
        for name, value in (("probability", self.probability), ("impact", self.impact), ("urgency", self.urgency), ("financial_impact", self.financial_impact)):
            if not 0 <= value <= 100:
                raise ValueError(f"{name} must be 0-100")

    @property
    def condition_risk(self) -> float:
        return round((self.condition_score - 1) / 5 * 100, 2)

    @property
    def risk_score(self) -> float:
        """Combine technical condition, probability, impact and urgency."""
        return round(
            0.30 * self.condition_risk
            + 0.25 * self.probability
            + 0.25 * self.impact
            + 0.10 * self.urgency
            + 0.10 * self.financial_impact,
            2,
        )

    @property
    def priority(self) -> str:
        if self.risk_score >= 75:
            return "KRITIEK"
        if self.risk_score >= 50:
            return "HOOG"
        if self.risk_score >= 25:
            return "NORMAAL"
        return "LAAG"


def risk_matrix_score(probability: float, impact: float) -> float:
    """Calculate a simple probability x impact risk score on a 0-100 scale."""
    if not 0 <= probability <= 100 or not 0 <= impact <= 100:
        raise ValueError("probability and impact must be 0-100")
    return round(probability * impact / 100, 2)


def sort_risks(assessments: list[RiskAssessment]) -> list[RiskAssessment]:
    """Return highest-priority risks first."""
    return sorted(assessments, key=lambda item: item.risk_score, reverse=True)
