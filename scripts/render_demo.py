#!/usr/bin/env python3
"""Attempt a low-quality render of the Part 1 demonstration scene."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DEMO = ROOT / "examples" / "foundation_demo.py"


def preflight() -> list[str]:
    problems: list[str] = []
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    from quonitron_manim.core.manim_compat import cairo_usable, manimpango_usable

    ok, msg = cairo_usable()
    if not ok:
        problems.append(msg)
    ok, msg = manimpango_usable()
    if not ok:
        problems.append(msg)
    if shutil.which("ffmpeg") is None:
        problems.append("ffmpeg is not on PATH")
    if shutil.which("manim") is None:
        # Fall back to python -m manim
        try:
            import manim  # noqa: F401
        except Exception as exc:  # noqa: BLE001
            problems.append(f"manim import failed: {exc}")
    return problems


def main() -> int:
    problems = preflight()
    if problems:
        print("SKIP render: environment cannot run Manim.")
        for item in problems:
            print(f"  - {item}")
        print(
            "Install Cairo, Pango, FFmpeg, and manim, then re-run:\n"
            "  python scripts/render_demo.py\n"
            "  manim -ql examples/foundation_demo.py VariableStoresAValue"
        )
        return 2

    cmd = [
        sys.executable,
        "-m",
        "manim",
        "-ql",
        "--disable_caching",
        str(DEMO),
        "VariableStoresAValue",
    ]
    print("Running:", " ".join(cmd))
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC) + (
        (os.pathsep + env["PYTHONPATH"]) if env.get("PYTHONPATH") else ""
    )
    completed = subprocess.run(cmd, cwd=str(ROOT), env=env)
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
