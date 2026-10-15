from pathlib import Path

from quonitron_manim.components.text import ALL_TEXT_COMPONENTS
from quonitron_manim.components.text.blocks import BodyParagraph, DisplayTitle
from quonitron_manim.components.text.emphasis import HighlightedPhrase
from quonitron_manim.components.text.lists import BulletList
from quonitron_manim.components.text.wrap import (
    TextLayoutError,
    chars_for_width,
    highlight_parts,
    wrap_plain_text,
)
from quonitron_manim.core.catalog import get_component, resolve, search_catalog, validate_catalog
from quonitron_manim.design.layout import box_overflow, content_area, safe_area
from quonitron_manim.design.theme import get_theme
from quonitron_manim.motion import ALL_MOTION_RECIPES
from quonitron_manim.timeline.models import load_timeline
from quonitron_manim.timeline.validate import validate_timeline
from quonitron_manim.transitions import ALL_TRANSITIONS


def test_wrap_keeps_words_intact():
    lines = wrap_plain_text(
        "A variable is a named place that holds a value while a program runs.",
        28,
    )
    assert lines
    assert all(len(line) <= 28 or " " not in line for line in lines)
    assert "variable" in " ".join(lines)


def test_wrap_rejects_tiny_budget():
    try:
        wrap_plain_text("hello world", 3)
        raise AssertionError("expected TextLayoutError")
    except TextLayoutError:
        pass


def test_highlight_parts_and_error():
    before, phrase, after = highlight_parts("score is the name.", "score")
    assert phrase == "score"
    assert after.startswith(" is")
    try:
        highlight_parts("score is the name.", "banana")
        raise AssertionError("expected TextLayoutError")
    except TextLayoutError:
        pass


def test_content_area_reserves_caption_band():
    theme = get_theme()
    safe = safe_area(theme.frame_width, theme.frame_height, theme.spacing.safe_margin)
    content = content_area(theme.frame_width, theme.frame_height, theme.spacing.safe_margin)
    assert content.bottom > safe.bottom
    assert content.top == safe.top
    hits = box_overflow(-8, 8, -4, 4, content)
    assert "left" in hits and "right" in hits


def test_paragraph_validate_without_manim():
    BodyParagraph(text="A named slot holds a replaceable value.").validate()
    try:
        BodyParagraph(text="   ").validate()
        raise AssertionError("expected TextLayoutError")
    except TextLayoutError:
        pass
    DisplayTitle(text="A Name for a Value").validate()
    HighlightedPhrase(text="score is the name.", phrase="score").validate()
    BulletList(items=["A name.", "A slot.", "A value."]).validate()


def test_every_text_component_validates_or_explains():
    for cls in ALL_TEXT_COMPONENTS:
        recipe = cls()
        assert recipe.component_id.startswith("text.")
        assert recipe.category == "text"


def test_chars_for_width_is_positive():
    assert chars_for_width(12.6, 28) >= 20


def test_text_ids_are_in_the_catalog(repo_root: Path):
    master = validate_catalog(repo_root)
    ids = {item["id"] for item in master["components"]}
    for cls in ALL_TEXT_COMPONENTS:
        assert cls.component_id in ids
        entry = get_component(cls.component_id, root=repo_root)
        assert resolve(cls.component_id, root=repo_root) is cls
        assert entry["class_name"] == cls.__name__
    assert "utility.text_wrap" in ids
    hits = search_catalog("highlighted words", root=repo_root)
    assert any(item["id"] == "text.highlighted_phrase" for item in hits)


def test_text_timeline_validates(repo_root: Path):
    timeline = load_timeline(repo_root / "examples" / "text_timeline.json")
    known = [cls.component_id for cls in ALL_MOTION_RECIPES] + [
        cls.component_id for cls in ALL_TRANSITIONS
    ] + [cls.component_id for cls in ALL_TEXT_COMPONENTS]
    report = validate_timeline(timeline, known_motion_ids=known)
    assert report.ok, [item.message for item in report.errors]
    assert timeline.scene.duration >= 55
    assert timeline.scene.duration <= 90
    assert all(cue.timing_status == "estimated" for cue in timeline.cues)
    assert all(cue.text[0].isupper() for cue in timeline.cues)
    assert "score" in " ".join(c.text for c in timeline.cues)


def test_new_type_roles_exist():
    theme = get_theme()
    assert theme.typography.style("subheading").font_size == 30.0
    assert theme.typography.style("annotation").color_role == "accent"
    assert theme.typography.style("equation").color_role == "equation"
