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
