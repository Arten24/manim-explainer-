"""Render existing demos and extract representative frames; no false visual pass.

Run from repository root: python scripts/render_layout_audit.py
Outputs are ignored under media/layout-audit/. Review PNGs manually.
"""
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CASES = [
    ("foundation_demo.py", "VariableStoresAValue", [1, 5, 12, 20]),
    ("motion_timeline_demo.py", "VariableMemoryTimeline", [5, 34, 59.4, 60, 95]),
    ("journey_demo.py", "CodeToMemoryJourney", [10, 22.8, 41, 49, 54, 65]),
    ("text_typography_demo.py", "AssignmentInType", [3, 9, 28, 32, 38.3, 43.5, 47.6, 53]),
    ("layout_audit_demo.py", "LayoutRepairExercise", [1, 3.1, 3.6, 5]),
]


def main():
    from quonitron_manim.core.manim_compat import cairo_usable, manimpango_usable
    checks = [cairo_usable(), manimpango_usable()]
    if not all(ok for ok, _ in checks) or not shutil.which("ffmpeg"):
        print("BLOCKED: actual renders/frames not verified:", checks, "ffmpeg:", shutil.which("ffmpeg"))
        return 2
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
    media = ROOT / "media" / "layout-audit"
    for filename, scene, timestamps in CASES:
        subprocess.run([sys.executable, "-m", "manim", "-ql", "--media_dir", str(media),
                        str(ROOT / "examples" / filename), scene], cwd=ROOT, env=env, check=True)
        videos = [p for p in media.rglob(scene + ".mp4") if "partial_movie_files" not in str(p)]
        video = max(videos, key=lambda p: p.stat().st_mtime)
        frames = media / "frames" / scene
        frames.mkdir(parents=True, exist_ok=True)
        for timestamp in timestamps:
            subprocess.run(["ffmpeg", "-y", "-ss", str(timestamp), "-i", str(video),
                            "-frames:v", "1", str(frames / f"{timestamp:06.2f}.png")], check=True)
    print("Frames extracted, NOT visually approved. Inspect media/layout-audit/frames.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
