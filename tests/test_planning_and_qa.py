from quonitron.planning import split_script
from quonitron.qa import run_all_checks
from quonitron.render import RenderConfig


def test_split_script_by_headings():
    script = """
Scene 1: What is a derivative?
A derivative measures how a function changes.

Scene 2: Gradient descent
Gradient descent uses derivatives to walk downhill on a loss surface.
"""
    scenes = split_script(script)
    assert len(scenes) == 2
    assert scenes[0].scene_id == "scene_001"
    assert "derivative" in scenes[0].title.lower()
    assert any("gradient descent" in q for q in scenes[1].suggested_queries)


def test_qa_checks_pass():
    results = run_all_checks()
    failed = [item.as_line() for item in results if not item.passed]
    assert failed == [], failed


def test_render_config_preview_uses_theme_background():
    cfg = RenderConfig.preview_defaults()
    assert cfg.background_color == "#0B0F19"
    assert cfg.pixel_width < 1920
    prod = RenderConfig.production_defaults()
    assert prod.pixel_width == 1920
    assert prod.frame_rate == 30
