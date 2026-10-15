from quonitron_manim.config import get_render_profile
from quonitron_manim.design import (
    get_theme,
    list_themes,
    resolve_font,
    safe_area,
)
from quonitron_manim.design.motion import EASING_ALIASES
from quonitron_manim.design.theme import ColorPalette, register_theme


def test_default_theme_matches_part1_spec():
    assert "quonitron_dark" in list_themes()
    theme = get_theme()
    assert theme.color("background") == "#0D1117"
    assert theme.color("text_primary") == "#F5F7FA"
    assert theme.color("text_secondary") == "#9AA4B2"
    assert theme.color("accent") == "#4C8DFF"
    assert theme.duration("normal") == 0.6
    assert theme.typography.style("title").font_size == 48.0
    assert theme.spacing.safe_margin > theme.spacing.margin


def test_unknown_color_role_fails():
    theme = get_theme()
    try:
        theme.color("neon_soup")
        raise AssertionError("expected ValueError")
    except ValueError as exc:
        assert "neon_soup" in str(exc)


def test_theme_override_does_not_mutate_default():
    base = get_theme()
    custom = base.override(name="custom_dark", colors={"accent": "#5B9BFF"})
    register_theme("custom_dark", custom)
    assert get_theme().color("accent") == "#4C8DFF"
    assert get_theme("custom_dark").color("accent") == "#5B9BFF"
    assert get_theme("custom_dark").color("background") == "#0D1117"


def test_safe_area_is_inside_frame():
    theme = get_theme()
    area = safe_area(theme.frame_width, theme.frame_height, theme.spacing.safe_margin)
    assert area.width < theme.frame_width
    assert area.height < theme.frame_height
    assert area.left < 0 < area.right
    assert area.bottom < 0 < area.top


def test_font_fallback_uses_first_available():
    chosen = resolve_font(["Definitely Missing Font", "Arial"], available=["Arial", "Calibri"])
    assert chosen == "Arial"
    fallback = resolve_font(["Inter", "DejaVu Sans"], available=[])
    assert fallback == "Inter"


def test_render_profile_preview_is_cheap():
    preview = get_render_profile("ql")
    assert preview.pixel_height == 480
    assert preview.frame_rate == 15
    prod = get_render_profile("production")
    assert prod.pixel_width == 1920


def test_easing_aliases_cover_defaults():
    theme = get_theme()
    assert theme.motion.easing_default in EASING_ALIASES
    assert theme.motion.easing_entrance in EASING_ALIASES


def test_palette_hex_values():
    palette = ColorPalette()
    for role in palette.__dataclass_fields__:
        value = getattr(palette, role)
        assert value.startswith("#")
        assert len(value) in (4, 7, 9)
