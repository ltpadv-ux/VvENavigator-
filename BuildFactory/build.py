#!/usr/bin/env python3
"""VvE Navigator BuildFactory command-line entry point."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

VERSION = "1.7.0"
ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "config" / "navigator.json"


def load_config() -> dict:
    if not CONFIG.exists():
        return {}
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def cmd_version() -> int:
    print(f"VvE Navigator BuildFactory {VERSION}")
    return 0


def cmd_init() -> int:
    for directory in (ROOT / "config", ROOT / "src", ROOT / "tests", ROOT / "data"):
        directory.mkdir(parents=True, exist_ok=True)
    print("BuildFactory initialized")
    return 0


def cmd_doctor() -> int:
    checks = {
        "config": CONFIG.exists(), "python": True, "source": (ROOT / "src").exists(),
        "tests": (ROOT / "tests").exists(), "data": (ROOT / "data").exists(),
        "mjop_engine": (ROOT / "src" / "mjop_engine.py").exists(),
        "finance_engine": (ROOT / "src" / "finance_engine.py").exists(),
        "financial_cockpit": (ROOT / "src" / "financial_cockpit.py").exists(),
        "risk_engine": (ROOT / "src" / "risk_engine.py").exists(),
        "decision_engine": (ROOT / "src" / "decision_engine.py").exists(),
        "governance_engine": (ROOT / "src" / "governance_engine.py").exists(),
        "action_engine": (ROOT / "src" / "action_engine.py").exists(),
        "audit_engine": (ROOT / "src" / "audit_engine.py").exists(),
        "dashboard_engine": (ROOT / "src" / "dashboard_engine.py").exists(), "report_engine": (ROOT / "src" / "report_engine.py").exists(),
        "datahub": (ROOT / "src" / "datahub.py").exists(), "export_engine": (ROOT / "src" / "export_engine.py").exists(),
        "excel_master": (ROOT / "src" / "excel_master.py").exists(), "navigator_mvp": (ROOT / "src" / "navigator_mvp.py").exists(),
        "scenario_engine": (ROOT / "src" / "scenario_engine.py").exists(),
        "practice_dataset": (ROOT / "src" / "practice_dataset.py").exists(),
        "sample_vve_34": (ROOT / "data" / "sample_vve_34.json").exists(),
    }
    for name, ok in checks.items():
        print(f"[{'OK' if ok else 'FAIL'}] {name}")
    return 0 if all(checks.values()) else 1


def cmd_status() -> int:
    config = load_config()
    print(json.dumps({"version": VERSION, "project": config.get("project", {}), "modules": config.get("modules", [])}, indent=2, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="build.py", description="VvE Navigator BuildFactory")
    parser.add_argument("command", choices=("init", "doctor", "version", "status"))
    args = parser.parse_args()
    return {"init": cmd_init, "doctor": cmd_doctor, "version": cmd_version, "status": cmd_status}[args.command]()


if __name__ == "__main__":
    raise SystemExit(main())
