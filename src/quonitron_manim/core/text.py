"""Theme-aware Manim text helpers with font fallbacks."""

from __future__ import annotations

from typing import Any, Optional

from quonitron_manim.design.theme import Theme, get_theme
from quonitron_manim.design.typography import resolve_font


def themed_text(
    content: str,
    role: str = "body",
    theme: Optional[Theme] = None,
    *,
    color_role: Optional[str] = None,
    font_size: Optional[float] = None,
    **kwargs: Any,
):
    """Build a Manim ``Text`` mobject using the design system.

    Raises ImportError if Manim/Pango is unavailable. Callers that only
    need layout math should not use this helper.
    """
    from manim import Text

    theme = theme or get_theme()
    style = theme.typography.style(role)
    stack = theme.typography.family_stack(style.family)
    font = resolve_font(stack)
    color = theme.color(color_role or style.color_role)
    weight = kwargs.pop("weight", style.weight)
    slant = kwargs.pop("slant", style.slant)
    return Text(
        content,
        font=font,
        font_size=font_size if font_size is not None else style.font_size,
        color=color,
        weight=weight,
        slant=slant,
        line_spacing=theme.typography.line_spacing,
        warn_missing_font=False,
        **kwargs,
    )


def fit_to_width(mobject: Any, max_width: float) -> Any:
    """Scale a mobject down if it is wider than ``max_width``. Never scales up."""
    if max_width <= 0:
        raise ValueError("max_width must be positive")
    width = float(getattr(mobject, "width", 0) or 0)
    if width > max_width:
        mobject.scale(max_width / width)
    return mobject


def measured_text(content: str, role="body", theme=None, *, max_width: float,
                  max_height=None, max_lines=None, buff=0.12, **kwargs):
    """Greedy Pango-measured wrapping at the requested font size, never scaling.

    Explicit newlines are preserved. Oversized tokens split by character. Text too
    tall fails clearly instead of leaking into the caption band or shrinking type.
    """
    from manim import DOWN, LEFT, VGroup
    from quonitron_manim.design.layout import LayoutError
    if max_width <= 0:
        raise LayoutError("max_width must be positive")
    theme = theme or get_theme()
    lines = []
    def make(text):
        return themed_text(text, role, theme, **kwargs)
    for paragraph in str(content).split("\n"):
        current = ""
        if not paragraph.strip():
            # An invisible glyph preserves a blank line's measured height.
            lines.append(make("M").set_opacity(0))
            continue
        for word in paragraph.split():
            candidate = (current + " " + word).strip()
            if make(candidate).width <= max_width:
                current = candidate
                continue
            if current:
                lines.append(make(current))
                current = ""
            for char in word:
                if make(char).width > max_width:
                    raise LayoutError("Region narrower than a single glyph")
                if current and make(current + char).width > max_width:
                    lines.append(make(current))
                    current = ""
                current += char
        if current:
            lines.append(make(current))
    if max_lines is not None and len(lines) > max_lines:
        raise LayoutError(f"{role} needs {len(lines)} lines; limit {max_lines}. Split the cue; font size was preserved.")
    group = VGroup(*lines).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    if max_height is not None and group.height > max_height + 1e-6:
        raise LayoutError(f"{role} text needs {group.height:.3f} units; available "
                          f"{max_height:.3f}. Split the explanation/cue; font size was preserved.")
    group.measured_line_count = len(lines)
    return group


def subtitle_text(content, theme=None, *, style=None, **kwargs):
    """Fixed-size, measured, bottom-aligned subtitle; never shrink to fit."""
    from quonitron_manim.design.layout import place_in
    from quonitron_manim.subtitles.models import SubtitleStyle
    theme = theme or get_theme()
    style = style or SubtitleStyle()
    area = style.region(theme)
    mob = measured_text(content or " ", "caption", theme, max_width=area.width,
                        max_height=area.height, max_lines=style.max_lines,
                        buff=style.line_gap, **kwargs)
    place_in(mob, area, align="bottom")
    mob.set_z_index(100)
    return mob
