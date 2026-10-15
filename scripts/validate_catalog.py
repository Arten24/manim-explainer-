#!/usr/bin/env python3
"""Validate the master catalog and print a QA report."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from quonitron.qa import report, run_all_checks


def main() -> int:
    print(report())
    results = run_all_checks()
    return 0 if all(item.passed for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
