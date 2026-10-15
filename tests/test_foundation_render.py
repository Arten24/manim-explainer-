import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from quonitron_manim.core.base_scene import QuonitronScene
from quonitron_manim.core.component import Component
from quonitron_manim.core.manim_compat import cairo_usable, import_error_message, manimpango_usable
from quonitron_manim.components.foundation import SectionHeading, TitleCard, VariableStore


def test_base_scene_imports_and_exposes_helpers():
    assert issubclass(QuonitronScene, object)
    for name in (
        "make_title",
        "make_heading",
        "make_body",
        "make_label",
        "make_caption",
        "show_subtitle_text",
        "play_entrance",
    ):
        assert callable(getattr(QuonitronScene, name))


def test_foundation_components_are_registered():
    assert TitleCard.component_id == "foundation.title_card"
    assert SectionHeading.component_id == "foundation.section_heading"
    assert VariableStore.component_id == "foundation.variable_store"
    assert issubclass(TitleCard, Component)


def test_demo_scene_class_is_loadable(repo_root: Path):
    path = repo_root / "examples" / "foundation_demo.py"
    spec = importlib.util.spec_from_file_location("foundation_demo", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    scene_cls = module.VariableStoresAValue
    assert issubclass(scene_cls, QuonitronScene)
    assert callable(scene_cls.construct)


def test_demo_uses_theme_not_hardcoded_hex(repo_root: Path):
    source = (repo_root / "examples" / "foundation_demo.py").read_text(encoding="utf-8")
    assert "get_theme" in source or "self.theme" in source
    assert "#0D1117" not in source
    assert "#F5F7FA" not in source


@pytest.mark.render
def test_low_quality_preview_render(repo_root: Path, tmp_path: Path):
    cairo_ok, cairo_msg = cairo_usable()
    pango_ok, pango_msg = manimpango_usable()
    if not cairo_ok or not pango_ok:
        pytest.skip(
            "Manim preview render requires Cairo and Pango: "
            f"{cairo_msg}; {pango_msg}"
        )
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
        str(repo_root / "examples" / "foundation_demo.py"),
        "VariableStoresAValue",
    ]
    completed = subprocess.run(
        cmd,
        cwd=str(repo_root),
        env=env,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        pytest.fail(
            "Preview render failed.\n"
            f"stdout:\n{completed.stdout[-2000:]}\n"
            f"stderr:\n{completed.stderr[-2000:]}"
        )
    videos = list(media.rglob("*.mp4"))
    assert videos, "Render reported success but produced no mp4"


def test_render_limitation_is_detectable():
    # Always runs: documents why a render test may skip.
    message = import_error_message()
    cairo_ok, _ = cairo_usable()
    if cairo_ok:
        assert message is None or "manimpango" in message
    else:
        assert message
