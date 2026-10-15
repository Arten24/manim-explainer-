"""Branded opening title used across QUONITRON explainers."""

from __future__ import annotations

from typing import Any

from quonitron_manim.core.component import Component, register_component
from quonitron_manim.core.text import themed_text
from quonitron_manim.design.typography import resolve_font


@register_component
class TitleCard(Component):
    """Centered title with a thin accent rule and optional kicker."""

    component_id = "foundation.title_card"
    name = "Title Card"
    category = "foundation"
    version = "0.2.0"

    def build(self) -> Any:
        from manim import DOWN, ORIGIN, UP, Line, VGroup

        title = self.param("title", "QUONITRON")
        kicker = self.param("kicker", "QUONITRON")
        include_kicker = self.param("include_kicker", True)
        theme = self.theme

        title_mob = themed_text(title, "title", theme)
        rule_width = max(title_mob.width * 0.42, 1.6)
        rule = Line(
            start=[-rule_width / 2, 0, 0],
            end=[rule_width / 2, 0, 0],
            color=theme.color("accent"),
            stroke_width=theme.stroke.regular,
        )

        parts = []
        if include_kicker:
            kicker_mob = themed_text(kicker, "label", theme, color_role="accent")
            # Small tracking look: keep kicker above the rule.
            kicker_mob.next_to(rule, UP, buff=theme.spacing.sm)
            parts.append(kicker_mob)
        title_mob.next_to(rule, DOWN, buff=theme.spacing.sm)
        parts.extend([rule, title_mob])
        group = VGroup(*parts)
        group.move_to(ORIGIN)
        # Font is resolved so missing Inter/custom faces do not crash.
        _ = resolve_font(theme.typography.font_sans)
        return group
