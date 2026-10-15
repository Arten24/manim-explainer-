"""Simple visual: a named box that holds a value.

Used in the Part 1 demo to show how a variable stores a value.
"""

from __future__ import annotations

from typing import Any

from quonitron_manim.core.component import Component, register_component
from quonitron_manim.core.text import themed_text


@register_component
class VariableStore(Component):
    """Rounded card with a variable name and a replaceable value."""

    component_id = "foundation.variable_store"
    name = "Variable Store"
    category = "foundation"
    version = "0.2.0"

    def build(self) -> Any:
        from manim import DOWN, UP, RoundedRectangle, VGroup

        theme = self.theme
        name = str(self.param("variable_name", "score"))
        value = str(self.param("value", "0"))
        width = float(self.param("width", 4.6))
        height = float(self.param("height", 2.4))

        card = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=theme.stroke.corner_radius,
            color=theme.color("border"),
            stroke_width=theme.stroke.regular,
            fill_color=theme.color("surface"),
            fill_opacity=1.0,
        )
        name_mob = themed_text(name, "label", theme, color_role="text_secondary")
        value_mob = themed_text(value, "title", theme, color_role="highlight")
        name_mob.next_to(card.get_top(), DOWN, buff=theme.spacing.sm)
        value_mob.move_to(card.get_center())
        value_mob.shift(DOWN * 0.12)

        group = VGroup(card, name_mob, value_mob)
        group.name_label = name_mob  # type: ignore[attr-defined]
        group.value_label = value_mob  # type: ignore[attr-defined]
        group.card = card  # type: ignore[attr-defined]
        return group

    def make_value(self, value: str) -> Any:
        """Build a replacement value mobject styled like the original."""
        return themed_text(str(value), "title", self.theme, color_role="highlight")
