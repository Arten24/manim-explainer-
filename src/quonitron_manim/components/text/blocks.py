"""Titles, headings, paragraphs, captions."""

from __future__ import annotations

from typing import Any

from quonitron_manim.components.text.base import TextComponent, text_component
from quonitron_manim.components.text.wrap import TextLayoutError, wrap_plain_text
from quonitron_manim.core.text import themed_text


def stacked_lines(lines: list[str], role: str, theme, buff: float):
    from manim import DOWN, LEFT, VGroup

    mobs = [themed_text(line, role, theme) for line in lines]
    group = VGroup(*mobs)
    if len(mobs) > 1:
        group.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    return group


@text_component
class DisplayTitle(TextComponent):
    """In-scene title using the type hierarchy. Prefer TitleCard for branded openings."""

    component_id = "text.display_title"
    name = "Display Title"
    subcategory = "block"
    tags = ["title", "typography"]
    aliases = ["main title", "display title"]
    use_cases = ["Name the current explanation without the full title card"]
    related = ["foundation.title_card", "design.theme.quonitron_dark"]
    parameters_schema = {
        "text": {"type": "string", "description": "Title copy", "default": "Title"}
    }

    def validate(self) -> None:
        super().validate()
        if not str(self.param("text", "Title")).strip():
            raise TextLayoutError("text.display_title needs non-empty text")

    def build(self) -> Any:
        self.validate()
        mob = themed_text(str(self.param("text", "Title")).strip(), "title", self.theme)
        return self.clamp_to_content(mob)


@text_component
class SceneHeading(TextComponent):
    """Section heading with an optional accent marker."""

    component_id = "text.heading"
    name = "Scene Heading"
    subcategory = "block"
    tags = ["heading", "typography"]
    aliases = ["section heading", "heading"]
    related = ["foundation.section_heading", "design.theme.quonitron_dark"]
    parameters_schema = {
        "text": {"type": "string", "description": "Heading copy", "default": "Heading"},
        "marker": {
            "type": "boolean",
            "description": "Draw the accent bar used by foundation.section_heading",
            "default": True,
        },
    }

    def validate(self) -> None:
        super().validate()
        if not str(self.param("text", "Heading")).strip():
            raise TextLayoutError("text.heading needs non-empty text")

    def build(self) -> Any:
        self.validate()
        from manim import LEFT, RIGHT, RoundedRectangle, VGroup

        heading = themed_text(str(self.param("text")).strip(), "heading", self.theme)
        if not bool(self.param("marker", True)):
            return self.clamp_to_content(heading)
        marker = RoundedRectangle(
            width=0.12,
            height=heading.height,
            corner_radius=0.03,
            color=self.theme.color("accent"),
            fill_color=self.theme.color("accent"),
            fill_opacity=1.0,
            stroke_width=0,
        )
        group = VGroup(marker, heading).arrange(RIGHT, buff=self.theme.spacing.sm)
        return self.clamp_to_content(group)


@text_component
class Subheading(TextComponent):
    """Secondary heading under a section title."""

    component_id = "text.subheading"
    name = "Subheading"
    subcategory = "block"
    tags = ["subheading", "typography"]
    aliases = ["subheading", "explanatory heading"]
    parameters_schema = {
        "text": {"type": "string", "description": "Subheading copy", "default": "Subheading"}
    }

    def validate(self) -> None:
        super().validate()
        if not str(self.param("text", "")).strip():
            raise TextLayoutError("text.subheading needs non-empty text")

    def build(self) -> Any:
        self.validate()
        mob = themed_text(str(self.param("text")).strip(), "subheading", self.theme)
        return self.clamp_to_content(mob)


@text_component
class BodyParagraph(TextComponent):
    """Wrapped explanatory paragraph that stays inside the content area."""

    component_id = "text.paragraph"
    name = "Body Paragraph"
    subcategory = "block"
    tags = ["paragraph", "wrap", "body"]
    aliases = ["paragraph", "explanatory text", "wrapped body"]
    use_cases = ["A teacher sentence that must not run off the frame"]
    parameters_schema = {
        "text": {"type": "string", "description": "Paragraph copy"},
        "role": {
            "type": "string",
            "description": "Type role",
            "default": "body",
            "enum": ["body", "label", "caption"],
        },
    }

    def lines(self) -> list[str]:
        text = str(self.param("text", "")).strip()
        if not text:
            raise TextLayoutError("text.paragraph needs non-empty text")
        role = str(self.param("role", "body"))
        return wrap_plain_text(text, self.max_chars_for(role))

    def validate(self) -> None:
        super().validate()
        self.lines()

    def build(self) -> Any:
        self.validate()
        role = str(self.param("role", "body"))
        group = stacked_lines(self.lines(), role, self.theme, self.theme.spacing.xs)
        group.lines = group  # type: ignore[attr-defined]
        return self.clamp_to_content(group)


@text_component
class EducationalCaption(TextComponent):
    """In-scene caption for a diagram. Not the SubtitleOverlay clock."""

    component_id = "text.caption"
    name = "Educational Caption"
    subcategory = "block"
    tags = ["caption", "label"]
    aliases = ["diagram caption"]
    limitations = (
        "This is educational copy next to a figure. Timed narration uses "
        "foundation.subtitle_overlay on the shared timeline."
    )
    related = ["foundation.subtitle_overlay", "design.theme.quonitron_dark"]
    parameters_schema = {
        "text": {"type": "string", "description": "Caption copy"}
    }

    def validate(self) -> None:
        super().validate()
        if not str(self.param("text", "")).strip():
            raise TextLayoutError("text.caption needs non-empty text")

    def build(self) -> Any:
        self.validate()
        lines = wrap_plain_text(str(self.param("text")).strip(), self.max_chars_for("caption"))
        group = stacked_lines(lines, "caption", self.theme, self.theme.spacing.xxs)
        return self.clamp_to_content(group)
