"""Section heading with an accent marker."""

from __future__ import annotations

from typing import Any

from quonitron_manim.core.component import Component, register_component
from quonitron_manim.core.text import themed_text


@register_component
class SectionHeading(Component):
    """Left-accented heading for in-scene sections."""

    component_id = "foundation.section_heading"
    name = "Section Heading"
    category = "foundation"
    version = "0.2.0"

    def build(self) -> Any:
        from manim import LEFT, RIGHT, RoundedRectangle, VGroup

        text = self.param("text", "Section")
        theme = self.theme
        heading = themed_text(text, "heading", theme)
        marker = RoundedRectangle(
            width=0.12,
            height=heading.height,
            corner_radius=0.03,
            color=theme.color("accent"),
            fill_color=theme.color("accent"),
            fill_opacity=1.0,
            stroke_width=0,
        )
        marker.next_to(heading, LEFT, buff=theme.spacing.sm)
        group = VGroup(marker, heading)
        group.arrange(RIGHT, buff=theme.spacing.sm)
        return group
