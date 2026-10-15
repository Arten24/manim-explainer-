"""Inline code and single-line statements."""

from __future__ import annotations

from typing import Any

from quonitron_manim.components.text.base import TextComponent, text_component
from quonitron_manim.components.text.wrap import TextLayoutError
from quonitron_manim.core.text import themed_text


@text_component
class InlineCode(TextComponent):
    """A short identifier or token in the mono stack."""

    component_id = "text.inline_code"
    name = "Inline Code"
    subcategory = "code"
    tags = ["code", "mono", "token"]
    aliases = ["inline code", "code label"]
    parameters_schema = {
        "text": {"type": "string", "description": "Token or short snippet", "default": "score"}
    }

    def validate(self) -> None:
        super().validate()
        if not str(self.param("text", "")).strip():
            raise TextLayoutError("text.inline_code needs non-empty text")

    def build(self) -> Any:
        self.validate()
        mob = themed_text(str(self.param("text")).strip(), "code", self.theme)
        return self.clamp_to_content(mob)


@text_component
class CodeLine(TextComponent):
    """One source line on a surface chip. Not a full syntax highlighter (Part 10)."""

    component_id = "text.code_line"
    name = "Code Line"
    subcategory = "code"
    tags = ["code", "statement", "mono"]
    aliases = ["code statement", "source line"]
    use_cases = ["Show score = 10 as the assignment being explained"]
    limitations = "Single line, no lexer. Full highlighters belong in Part 10."
    parameters_schema = {
        "text": {"type": "string", "description": "Source line", "default": "score = 10"}
    }

    def validate(self) -> None:
        super().validate()
        text = str(self.param("text", "")).strip()
        if not text:
            raise TextLayoutError("text.code_line needs non-empty text")
        if "\n" in text:
            raise TextLayoutError("text.code_line is a single line")

    def build(self) -> Any:
        self.validate()
        from manim import RoundedRectangle, VGroup

        theme = self.theme
        label = themed_text(str(self.param("text")).strip(), "code", theme)
        pad = theme.spacing.card_padding
        chip = RoundedRectangle(
            width=label.width + pad * 2,
            height=label.height + pad * 1.4,
            corner_radius=theme.stroke.corner_radius,
            color=theme.color("border"),
            stroke_width=theme.stroke.thin,
            fill_color=theme.color("code_bg"),
            fill_opacity=1.0,
        )
        label.move_to(chip.get_center())
        group = VGroup(chip, label)
        group.label = label  # type: ignore[attr-defined]
        group.chip = chip  # type: ignore[attr-defined]
        return self.clamp_to_content(group)
