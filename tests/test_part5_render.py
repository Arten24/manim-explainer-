"""Native Pango and Cairo checks; absence is a reported skip, never visual approval."""
from pathlib import Path
import pytest

pytestmark = pytest.mark.render


def native():
    return pytest.importorskip("manim", reason="Part 5 native checks need Manim/Cairo/Pango")


def test_measured_subtitles_never_shrink_and_fail_on_overflow():
    native()
    from quonitron_manim.core.text import subtitle_text
    from quonitron_manim.subtitles.models import SubtitleStyle
    from quonitron_manim.design.theme import get_theme
    from quonitron_manim.design.layout import LayoutError, bounds, box_overflow
    theme = get_theme()
    style = SubtitleStyle(max_lines=2, max_width=10)
    mob = subtitle_text("A name, a value — and punctuation!\nA second line.", theme, style=style)
    box, area = bounds(mob), style.region(theme)
    assert not box_overflow(box.left, box.right, box.bottom, box.top, area)
    assert mob.measured_line_count == 2
    assert all(line.font_size == pytest.approx(theme.typography.caption.font_size) for line in mob)
    with pytest.raises(LayoutError, match="font size was preserved"):
        subtitle_text("One\nTwo\nThree", theme, style=style)
    long = subtitle_text("longtoken" * 8, theme, style=SubtitleStyle(max_width=10, max_lines=2))
    assert long.width <= 10 + 1e-6


def test_simultaneous_speakers_preflight_and_camera_pin():
    native()
    from quonitron_manim.components.foundation.subtitle_overlay import SubtitleOverlay
    from quonitron_manim.subtitles.models import SubtitleStyle
    from quonitron_manim.timeline import LinkedCue, SceneWindow, Timeline
    from tests.test_part5_sync import cue
    from manim import Rectangle
    a, b = cue(speaker="A", overlap_ok=True), cue(id="b", sequence=2, speaker="B", overlap_ok=True)
    t = Timeline(SceneWindow("s", 0, 5), cues=[a, b], cue_overlap_policy="allow")
    overlay = SubtitleOverlay(style=SubtitleStyle(speaker_labels=True))
    measured = overlay.preflight(t)
    assert measured[overlay._active_text([a, b])] == 2
    frame = Rectangle(width=overlay.theme.frame_width, height=8).scale(.8).shift([1, .2, 0])
    class Scene:
        camera = type("Camera", (), {"frame": frame})()
    overlay.timeline = t
    overlay.get()
    overlay.update_at(2, scene=Scene())
    assert overlay._shown_id == (a.id, b.id)
    original = overlay._canonical.get_center()
    expected = original * .8 + frame.get_center()
    assert overlay._mob.get_center() == pytest.approx(expected)
    with pytest.raises(ValueError):
        SubtitleOverlay(style=SubtitleStyle(max_lines=1)).preflight(t)


def test_part5_actual_low_quality_render(tmp_path):
    manim = native()
    from examples.subtitle_sync_demo import SubtitleSyncDemo
    with manim.tempconfig({"quality": "low_quality", "media_dir": str(tmp_path),
                           "disable_caching": True, "write_to_movie": True,
                           "preview": False, "verbosity": "ERROR"}):
        scene = SubtitleSyncDemo()
        scene.render()
        assert Path(scene.renderer.file_writer.movie_file_path).stat().st_size > 0
        assert scene.sync_overlay._shown_id == ()
        assert not [i for i in scene.check_layout() if i.severity == "ERROR"]
