"""Section heading with an accent marker."""

from __future__ import annotations

from typing import Any

from quonitron_manim.core.component import Component, register_component
from quonitron_manim.core.text import measured_text


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
        from quonitron_manim.design.layout import content_area, place_in
        area = content_area(theme.frame_width, theme.frame_height, theme.spacing.safe_margin)
        heading = measured_text(text, "heading", theme,
                                max_width=area.width - 0.12 - theme.spacing.sm,
                                max_height=area.height)
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
        return place_in(group, area)
