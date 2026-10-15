#!/usr/bin/env python3
"""Low-quality render of the Part 3 journey demonstration."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DEMO = ROOT / "examples" / "journey_demo.py"


def main() -> int:
    sys.path.insert(0, str(SRC))
    from quonitron_manim.core.manim_compat import cairo_usable, manimpango_usable

    problems = []
    ok, msg = cairo_usable()
    if not ok:
        problems.append(msg)
    ok, msg = manimpango_usable()
    if not ok:
        problems.append(msg)
    if shutil.which("ffmpeg") is None:
        problems.append("ffmpeg is not on PATH")
    if problems:
        print("SKIP render: environment cannot run Manim.")
        for item in problems:
            print(f"  - {item}")
        print("  manim -ql examples/journey_demo.py CodeToMemoryJourney")
        return 2
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC) + (
        (os.pathsep + env["PYTHONPATH"]) if env.get("PYTHONPATH") else ""
    )
    cmd = [
        sys.executable,
        "-m",
        "manim",
        "-ql",
        "--disable_caching",
        str(DEMO),
        "CodeToMemoryJourney",
    ]
    print("Running:", " ".join(cmd))
    return subprocess.run(cmd, cwd=str(ROOT), env=env).returncode


if __name__ == "__main__":
    raise SystemExit(main())
