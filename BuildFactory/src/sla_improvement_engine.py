"""SLA root-cause analysis and improvement prioritization for VvE Navigator."""
from __future__ import annotations
from collections import Counter
from typing import Any

ENGINE_VERSION = "4.7.0"

CATEGORY_MAP = {
    "artifact_pdf": ("Rendering", "Controleer en stabiliseer PDF-rendering."),
    "artifact_docx": ("Rendering", "Controleer en stabiliseer DOCX-rendering."),
    "artifact_xlsx": ("Rendering", "Controleer en stabiliseer XLSX-rendering."),
    "distribution_zip": ("Packaging", "Verbeter release packaging en bestandsbundeling."),
    "sign_off_go": ("Release Validation", "Herstel voorwaarden voor formele sign-off."),
    "released_for_alv": ("Release Validation", "Controleer de ALV-vrijgavevoorwaarden."),
    "quality_gate": ("Compliance & Quality", "Pak structurele Quality Gate-afwijkingen in brondata en besluitvorming aan."),
}


def analyze_sla_root_causes(history: list[dict[str, Any]], diagnostics_history: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    diagnostics_history = diagnostics_history or []
    counters: Counter[str] = Counter()
    category_counters: Counter[str] = Counter()

    for run in diagnostics_history:
        for item in run.get("diagnostics", []) or []:
            check = str(item.get("check", "unknown"))
            counters[check] += 1
            category = CATEGORY_MAP.get(check, (str(item.get("module", "Overig")), "Onderzoek terugkerende fout."))[0]
            category_counters[category] += 1

    blocked_runs = sum(1 for x in history if x.get("control_status") == "GEBLOKKEERD")
    healed_runs = sum(1 for x in history if x.get("control_status") == "HERSTELD")
    quality_issues = sum(int(x.get("quality_issue_count", 0) or 0) for x in history)
    repairs = sum(int(x.get("repair_count", 0) or 0) for x in history)

    structural = []
    for check, count in counters.most_common():
        category, action = CATEGORY_MAP.get(check, ("Overig", "Onderzoek de terugkerende fout en definieer een structurele oplossing."))
        impact = count * 3
        if category == "Compliance & Quality": impact += quality_issues * 2
        if category == "Rendering": impact += repairs
        structural.append({
            "check": check,
            "category": category,
            "occurrences": count,
            "impact_score": impact,
            "priority": "HOOG" if impact >= 6 else "MIDDEL" if impact >= 3 else "LAAG",
            "recommended_action": action,
        })

    if not structural and blocked_runs:
        structural.append({
            "check": "blocked_runs",
            "category": "Release Control",
            "occurrences": blocked_runs,
            "impact_score": blocked_runs * 3,
            "priority": "HOOG" if blocked_runs >= 2 else "MIDDEL",
            "recommended_action": "Analyseer de geblokkeerde runs en leg per blocker een structurele herstelmaatregel vast.",
        })

    top = structural[0] if structural else None
    return {
        "sla_improvement_engine_version": ENGINE_VERSION,
        "status": "IMPROVEMENT_REQUIRED" if structural else "NO_STRUCTURAL_ISSUE",
        "runs_analyzed": len(history),
        "blocked_runs": blocked_runs,
        "healed_runs": healed_runs,
        "total_repairs": repairs,
        "total_quality_issues": quality_issues,
        "root_causes": structural,
        "dominant_root_cause": top or {},
        "improvement_priority": (top or {}).get("priority", "GEEN"),
        "next_action": (top or {}).get("recommended_action", "Geen structurele verbeteractie nodig."),
    }
