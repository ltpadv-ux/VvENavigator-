#!/usr/bin/env python3
"""Production entrypoint for VvE Navigator Enterprise 2.0.0."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from enterprise_core import ReleaseProfile, run_enterprise


def main() -> int:
    parser = argparse.ArgumentParser(description="VvE Navigator Enterprise 2.0.0")
    parser.add_argument("dataset", nargs="?", default=str(ROOT / "data" / "sample_vve_34.json"))
    parser.add_argument("--horizon", type=int, default=30)
    parser.add_argument("--profile", default="production")
    args = parser.parse_args()

    result = run_enterprise(args.dataset, ReleaseProfile(name=args.profile, horizon_years=args.horizon))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "READY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
