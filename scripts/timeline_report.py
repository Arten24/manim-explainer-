#!/usr/bin/env python3
"""Print and save an inspectable timeline report, plus SRT/VTT."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from quonitron_manim.timeline.export_subtitles import write_timeline_subtitles  # noqa: E402
from quonitron_manim.timeline.models import load_timeline  # noqa: E402
from quonitron_manim.timeline.report import write_timeline_report  # noqa: E402
from quonitron_manim.timeline.validate import validate_timeline  # noqa: E402
from quonitron_manim.motion import ALL_MOTION_RECIPES  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "timeline",
        nargs="?",
        default=str(ROOT / "examples" / "variable_timeline.json"),
    )
    parser.add_argument("--out", default=str(ROOT / "examples" / "variable_timeline_report.md"))
    args = parser.parse_args()
    timeline = load_timeline(args.timeline)
    known = [cls.component_id for cls in ALL_MOTION_RECIPES]
    report = validate_timeline(timeline, known_motion_ids=known)
    path = write_timeline_report(timeline, args.out)
    exports = write_timeline_subtitles(timeline, ROOT / "examples")
    print(path.read_text(encoding="utf-8")[:2500])
    print("...")
    print(f"Wrote {path}")
    print(f"Wrote {exports['srt']} and {exports['vtt']}")
    print("Validation:", "OK" if report.ok else "FAILED")
    for issue in report.errors:
        print(" ERROR", issue.message)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
