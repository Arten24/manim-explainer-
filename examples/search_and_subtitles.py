"""Foundation example: search the catalog and export estimated subtitles."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from quonitron.catalog import search_catalog
from quonitron.planning import split_script
from quonitron.subtitles import cues_from_sentences, to_srt


SCRIPT = """
Scene 1: What is a derivative?
A derivative measures how a function changes as its input changes.
It is the slope of the tangent line at a point.

Scene 2: Why gradient descent needs derivatives
Gradient descent uses those slopes to walk downhill on a loss surface.
Each step subtracts a scaled gradient from the current weights.
"""


def main() -> None:
    scenes = split_script(SCRIPT)
    print(f"Planned {len(scenes)} scene(s).")
    for scene in scenes:
        print(f"- {scene.scene_id}: {scene.title}")
        print(f"  queries: {scene.suggested_queries}")
        for query in scene.suggested_queries:
            hits = search_catalog(query)
            preview = ", ".join(item["id"] for item in hits[:5]) or "(none yet)"
            print(f"  catalog[{query!r}]: {preview}")

    sentences = [
        "A derivative measures how a function changes as its input changes.",
        "Gradient descent uses those slopes to walk downhill on a loss surface.",
    ]
    track = cues_from_sentences(sentences, scene_id="scene_001")
    srt = to_srt(track)
    out = Path(__file__).with_name("preview_estimated.srt")
    # Example prints SRT; writing media files is optional.
    print("\n--- estimated SRT (not synced to a speaker) ---")
    print(srt)
    print(f"(not written; would be {out})")


if __name__ == "__main__":
    main()
