"""Annotations, highlighted phrases, counters, and groups."""

from __future__ import annotations

from typing import Any, Sequence

from quonitron_manim.components.text.base import TextComponent, text_component
from quonitron_manim.components.text.blocks import stacked_lines
from quonitron_manim.components.text.wrap import TextLayoutError, highlight_parts, wrap_plain_text
from quonitron_manim.core.text import themed_text


@text_component
class AnnotationCallout(TextComponent):
    """Accent-bar callout for a short explanation beside a figure."""

    component_id = "text.annotation"
    name = "Annotation Callout"
    subcategory = "emphasis"
    tags = ["annotation", "callout", "label"]
    aliases = ["annotation", "explanatory label", "callout"]
    parameters_schema = {
        "text": {"type": "string", "description": "Callout copy"}
    }

    def lines(self):
        text = str(self.param("text", "")).strip()
        if not text:
            raise TextLayoutError("text.annotation needs non-empty text")
        return wrap_plain_text(text, self.max_chars_for("annotation"))

    def validate(self) -> None:
        super().validate()
        self.lines()

    def build(self) -> Any:
        self.validate()
        from manim import LEFT, RIGHT, RoundedRectangle, VGroup

        body = stacked_lines(self.lines(), "annotation", self.theme, self.theme.spacing.xxs)
        bar = RoundedRectangle(
            width=0.10,
            height=max(body.height, 0.4),
            corner_radius=0.03,
            color=self.theme.color("accent"),
            fill_color=self.theme.color("accent"),
            fill_opacity=1.0,
            stroke_width=0,
        )
        group = VGroup(bar, body).arrange(RIGHT, buff=self.theme.spacing.sm)
        group.body = body  # type: ignore[attr-defined]
        return self.clamp_to_content(group)


@text_component
class HighlightedPhrase(TextComponent):
    """A sentence with one phrase in the highlight color, exposed as ``.phrase``."""

    component_id = "text.highlighted_phrase"
    name = "Highlighted Phrase"
    subcategory = "emphasis"
    tags = ["highlight", "phrase", "emphasis"]
    aliases = ["highlighted words", "emphasize a phrase"]
    use_cases = ["Color the identifier in a spoken sentence while keeping the rest readable"]
    parameters_schema = {
        "text": {"type": "string", "description": "Full sentence"},
        "phrase": {"type": "string", "description": "Substring to highlight"},
    }

    def parts(self):
        return highlight_parts(str(self.param("text", "")), str(self.param("phrase", "")))

    def validate(self) -> None:
        super().validate()
        self.parts()

    def build(self) -> Any:
        self.validate()
        from manim import RIGHT, VGroup

        before, phrase, after = self.parts()
        bits = []
        if before.strip():
            bits.append(themed_text(before, "body", self.theme))
        phrase_mob = themed_text(phrase, "body", self.theme, color_role="highlight")
        bits.append(phrase_mob)
        if after.strip():
            bits.append(themed_text(after, "body", self.theme))
        group = VGroup(*bits).arrange(RIGHT, buff=0.08)
        group.phrase = phrase_mob  # type: ignore[attr-defined]
        return self.clamp_to_content(group)


@text_component
class CounterLabel(TextComponent):
    """Numeric value with an optional caption. Value is ``.value_mob`` for transforms."""

    component_id = "text.counter"
    name = "Counter Label"
    subcategory = "emphasis"
    tags = ["counter", "number", "value"]
    aliases = ["numeric label", "counter"]
    related = ["motion.util.changing_decimal", "design.theme.quonitron_dark"]
    parameters_schema = {
        "value": {"type": "string", "description": "Displayed value", "default": "10"},
        "label": {"type": "string", "description": "Caption under the number", "default": ""},
    }

    def validate(self) -> None:
        super().validate()
        if not str(self.param("value", "")).strip():
            raise TextLayoutError("text.counter needs a value")

    def build(self) -> Any:
        self.validate()
        from manim import DOWN, VGroup

        value = themed_text(str(self.param("value")).strip(), "title", self.theme, color_role="highlight")
        label_text = str(self.param("label", "") or "").strip()
        if label_text:
            caption = themed_text(label_text, "caption", self.theme)
            group = VGroup(value, caption).arrange(DOWN, buff=self.theme.spacing.xs)
        else:
            group = VGroup(value)
        group.value_mob = value  # type: ignore[attr-defined]
        return self.clamp_to_content(group)


@text_component
class TextStack(TextComponent):
    """Vertical stack of already-built mobjects using theme spacing."""

    component_id = "text.group"
    name = "Text Stack"
    subcategory = "layout"
    tags = ["group", "stack", "layout"]
    aliases = ["text grouping", "stack text"]
    parameters_schema = {
        "buff": {
            "type": "number",
            "description": "Gap in scene units. Default is theme.spacing.md",
            "minimum": 0,
        }
    }
    required_mobjects: bool = True

    def validate(self) -> None:
        super().validate()
        buff = self.params.get("buff")
        if buff is not None and float(buff) < 0:
            raise TextLayoutError("buff must be >= 0")

    def arrange(self, mobjects: Sequence[Any]) -> Any:
        self.validate()
        if not mobjects:
            raise TextLayoutError("text.group needs at least one mobject")
        from manim import DOWN, LEFT, VGroup

        buff = float(self.param("buff", self.theme.spacing.md))
        group = VGroup(*mobjects).arrange(DOWN, buff=buff, aligned_edge=LEFT)
        return self.clamp_to_content(group)

    def build(self) -> Any:
        raise TextLayoutError("text.group is arranged via arrange(*mobjects), not get()")
