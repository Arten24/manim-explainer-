"""Automated quality checks that do not require a full Manim render."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from quonitron.catalog.loader import (
    CATALOG_PATH,
    SCHEMA_PATH,
    CatalogError,
    check_python_references,
    load_catalog,
    validate_catalog,
)

ROOT = Path(__file__).resolve().parents[2]


@dataclass
class CheckResult:
    name: str
    passed: bool
    details: List[str] = field(default_factory=list)

    def as_line(self) -> str:
        mark = "PASS" if self.passed else "FAIL"
        extra = "" if not self.details else " | " + "; ".join(self.details)
        return f"[{mark}] {self.name}{extra}"


def check_catalog_schema() -> CheckResult:
    try:
        validate_catalog()
    except CatalogError as exc:
        return CheckResult("catalog_schema", False, [str(exc)])
    return CheckResult("catalog_schema", True, [f"ok {CATALOG_PATH.name}"])


def check_catalog_python_refs() -> CheckResult:
    errors = check_python_references()
    return CheckResult("catalog_python_refs", not errors, errors)


def check_schema_file_present() -> CheckResult:
    missing = [str(p) for p in (SCHEMA_PATH, CATALOG_PATH) if not p.is_file()]
    return CheckResult("catalog_files", not missing, missing)


def _python_files() -> List[Path]:
    skip = {".venv", "venv", "__pycache__", "media", "dist", "build"}
    files: List[Path] = []
    for path in (ROOT / "quonitron").rglob("*.py"):
        if any(part in skip for part in path.parts):
            continue
        files.append(path)
    return files


def check_python_syntax() -> CheckResult:
    errors: List[str] = []
    files = _python_files()
    for path in files:
        source = path.read_text(encoding="utf-8")
        try:
            ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{path.relative_to(ROOT)}:{exc.lineno}: {exc.msg}")
    return CheckResult(
        "python_syntax",
        not errors,
        errors or [f"{len(files)} files parsed"],
    )


def check_no_tested_without_module() -> CheckResult:
    catalog = load_catalog()
    errors = []
    for item in catalog.get("components", []):
        if item.get("test_status") == "tested" and not item.get("module"):
            errors.append(item["id"])
    return CheckResult("tested_has_module", not errors, errors)


def run_all_checks() -> List[CheckResult]:
    return [
        check_schema_file_present(),
        check_catalog_schema(),
        check_catalog_python_refs(),
        check_python_syntax(),
        check_no_tested_without_module(),
    ]


def report() -> str:
    results = run_all_checks()
    lines = [item.as_line() for item in results]
    failed = sum(1 for item in results if not item.passed)
    lines.append(f"{len(results) - failed}/{len(results)} checks passed")
    return "\n".join(lines)
