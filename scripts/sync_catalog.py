#!/usr/bin/env python3
"""Merge Part 2 motion/timeline entries into catalog/master.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from quonitron_manim.motion import ALL_MOTION_RECIPES  # noqa: E402

KEEP_PREFIXES = (
    "design.",
    "foundation.base_scene",
    "foundation.title_card",
    "foundation.section_heading",
    "foundation.variable_store",
    "utility.subtitle_track",
)


def extra_entries() -> list[dict]:
    return [
        {
            "id": "timeline.shared",
            "name": "Shared Scene Timeline",
            "version": "0.3.0",
            "category": "utility",
            "subcategory": "timeline",
            "tags": ["timeline", "clock", "subtitle", "event", "sync"],
            "aliases": ["shared timeline", "scene clock"],
            "description": "One timeline for visual events and subtitle cues, with estimated vs manual timing and cue-to-event links.",
            "use_cases": [
                "Keep captions and animations on the same clock",
                "Override cue times after recording voiceover without rewriting animation code",
            ],
            "module": "quonitron_manim.timeline.models",
            "class_name": "Timeline",
            "parameters": {
                "frame_rate": {
                    "type": "number",
                    "description": "Used only to convert seconds to frames",
                    "default": 30,
                }
            },
            "dependencies": ["python>=3.10"],
            "compatibility": {"python": ">=3.10", "manim": ">=0.18.1,<1.0"},
            "example": "examples/variable_timeline.json",
            "preview": None,
            "test_status": "passed",
            "limitations": "Playback adapter sequences play() calls; overlapping play windows must set overlap_ok.",
            "related_components": ["utility.subtitle_track", "foundation.subtitle_overlay"],
            "license": "MIT",
        },
        {
            "id": "foundation.subtitle_overlay",
            "name": "Subtitle Overlay",
            "version": "0.3.0",
            "category": "foundation",
            "subcategory": "subtitles",
            "tags": ["subtitle", "caption", "overlay", "safe-area"],
            "aliases": ["on-screen captions"],
            "description": "Bottom-safe caption mobject updated from Timeline.cue_at() on the shared clock.",
            "use_cases": ["Render the same cues that are exported to SRT/VTT"],
            "module": "quonitron_manim.components.foundation.subtitle_overlay",
            "class_name": "SubtitleOverlay",
            "parameters": {
                "text": {"type": "string", "description": "Initial caption", "default": " "}
            },
            "dependencies": ["manim>=0.18.1", "manimpango>=0.7"],
            "compatibility": {"python": ">=3.10", "manim": ">=0.18.1,<1.0"},
            "example": "examples/motion_timeline_demo.py",
            "preview": None,
            "test_status": "not_tested",
            "limitations": "Needs Pango/Cairo to build Text. Updater uses dt from play/wait.",
            "related_components": ["timeline.shared", "design.theme.quonitron_dark"],
            "license": "MIT",
        },
        {
            "id": "utility.narration_segmenter",
            "name": "Narration Segmenter",
            "version": "0.3.0",
            "category": "utility",
            "subcategory": "subtitles",
            "tags": ["subtitle", "segment", "narration", "wpm"],
            "aliases": ["split narration", "cue splitter"],
            "description": "Split a full English narration into readable cues with configurable limits and estimated durations.",
            "use_cases": ["Author many subtitle cues from one paragraph of explanation"],
            "module": "quonitron_manim.subtitles.segment",
            "function_name": "split_narration",
            "parameters": {
                "max_chars": {"type": "integer", "default": 84, "description": "Soft character limit per cue"},
                "reading_wpm": {"type": "integer", "default": 150, "description": "Estimated reading speed"}
            },
            "dependencies": ["python>=3.10"],
            "compatibility": {"python": ">=3.10"},
            "example": "examples/variable_narration.txt",
            "preview": None,
            "test_status": "passed",
            "limitations": "Does not call TTS or transcription. Durations are estimates.",
            "related_components": ["timeline.shared", "utility.subtitle_track"],
            "license": "MIT",
        },
    ]


def keep(item: dict) -> bool:
    cid = item["id"]
    return any(cid == p or cid.startswith(p) for p in KEEP_PREFIXES) and not cid.startswith(
        "motion."
    )


def main() -> int:
    path = ROOT / "catalog" / "master.json"
    master = json.loads(path.read_text(encoding="utf-8"))
    preserved = [item for item in master["components"] if keep(item)]
    motion = [cls.catalog_dict() for cls in ALL_MOTION_RECIPES]
    extras = extra_entries()
    seen = {}
    merged = []
    for item in preserved + extras + motion:
        if item["id"] in seen:
            raise SystemExit(f"duplicate {item['id']}")
        seen[item["id"]] = True
        merged.append(item)
    master["components"] = merged
    master["catalog_version"] = "1.2.0"
    master["library_version"] = "0.3.0"
    master["updated"] = "2026-10-15"
    master["notes"] = (
        "Part 2 adds the basic motion library and a shared subtitle/animation "
        "timeline. Visual motion animate() calls need Manim; parameter tests pass "
        "without Cairo. Foundation visual rows remain not_tested until a preview render succeeds."
    )
    path.write_text(json.dumps(master, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(merged)} components to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
