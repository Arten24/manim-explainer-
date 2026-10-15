#!/usr/bin/env python3
"""Validate catalog/master.json against its schema and Python references."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from quonitron_manim.core.catalog import (  # noqa: E402
    CatalogError,
    check_python_references,
    validate_catalog,
)


def main() -> int:
    try:
        master = validate_catalog(ROOT)
    except CatalogError as exc:
        print(f"FAIL catalog: {exc}")
        return 1
    errors = check_python_references(master, ROOT)
    count = len(master.get("components") or [])
    print(f"PASS schema  schema_version={master['schema_version']}  components={count}")
    if errors:
        print("FAIL python references:")
        for line in errors:
            print(f"  - {line}")
        return 1
    print("PASS python references")
    ids = [item["id"] for item in master["components"]]
    for cid in ids:
        print(f"  {cid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
