#!/usr/bin/env python3
"""Search catalog/master.json from the command line."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from quonitron_manim.core.catalog import search_catalog  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the QUONITRON catalog")
    parser.add_argument("query", nargs="*", help="Free-text query")
    parser.add_argument("--category", default=None)
    parser.add_argument("--tag", default=None)
    parser.add_argument("--status", dest="test_status", default=None)
    args = parser.parse_args()
    hits = search_catalog(
        " ".join(args.query),
        category=args.category,
        tag=args.tag,
        test_status=args.test_status,
        root=ROOT,
    )
    if not hits:
        print("No matching components.")
        return 1
    for item in hits:
        print(f"{item['id']:40}  [{item['test_status']}]  {item['name']}")
        print(f"  {item['description']}")
    print(f"\n{len(hits)} result(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
