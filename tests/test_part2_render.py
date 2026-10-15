import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from quonitron_manim.core.manim_compat import cairo_usable, manimpango_usable
from quonitron_manim.timeline.models import load_timeline


def test_demo_scene_is_loadable(repo_root: Path):
    path = repo_root / "examples" / "motion_timeline_demo.py"
    spec = importlib.util.spec_from_file_location("motion_timeline_demo", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert callable(module.VariableMemoryTimeline.construct)
    source = path.read_text(encoding="utf-8")
    assert "variable_timeline.json" in source
    assert "#0D1117" not in source
    assert "play_on_scene" in source


def test_demo_binders_cover_every_event(repo_root: Path):
    source = (repo_root / "examples" / "motion_timeline_demo.py").read_text(encoding="utf-8")
    timeline = load_timeline(repo_root / "examples" / "variable_timeline.json")
    for event in timeline.events:
        assert event.id in source, event.id


@pytest.mark.render
def test_part2_low_quality_render(repo_root: Path, tmp_path: Path):
    cairo_ok, cairo_msg = cairo_usable()
    pango_ok, pango_msg = manimpango_usable()
    if not cairo_ok or not pango_ok:
        pytest.skip(f"Manim preview render requires Cairo and Pango: {cairo_msg}; {pango_msg}")
    if shutil.which("ffmpeg") is None:
        pytest.skip("ffmpeg is not installed")
    env = os.environ.copy()
    src = str(repo_root / "src")
    env["PYTHONPATH"] = src + ((os.pathsep + env["PYTHONPATH"]) if env.get("PYTHONPATH") else "")
    media = tmp_path / "media"
    cmd = [
        sys.executable,
        "-m",
        "manim",
        "-ql",
        "--disable_caching",
        "--media_dir",
        str(media),
        str(repo_root / "examples" / "motion_timeline_demo.py"),
        "VariableMemoryTimeline",
    ]
    completed = subprocess.run(cmd, cwd=str(repo_root), env=env, capture_output=True, text=True)
    if completed.returncode != 0:
        pytest.fail(
            "Preview render failed.\n"
            f"stdout:\n{completed.stdout[-2000:]}\n"
            f"stderr:\n{completed.stderr[-2000:]}"
        )
    assert list(media.rglob("*.mp4")), "Render reported success but produced no mp4"
