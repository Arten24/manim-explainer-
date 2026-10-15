"""Bullets and numbered steps."""

from __future__ import annotations

from typing import Any, List

from quonitron_manim.components.text.base import TextComponent, text_component
from quonitron_manim.components.text.blocks import stacked_lines
from quonitron_manim.components.text.wrap import TextLayoutError, normalize_items, wrap_plain_text


@text_component
class BulletList(TextComponent):
    """Vertical bullet list with wrapped items."""

    component_id = "text.bullet_list"
    name = "Bullet List"
    subcategory = "list"
    tags = ["list", "bullets", "recap"]
    aliases = ["bullet points", "bullet list"]
    parameters_schema = {
        "items": {
            "type": "array",
            "description": "List of item strings",
        }
    }

    def lines(self) -> List[str]:
        items = normalize_items(self.param("items", []) or [])
        budget = max(8, self.max_chars_for("body") - 2)
        out: List[str] = []
        for item in items:
            wrapped = wrap_plain_text(item, budget)
            out.append("• " + wrapped[0])
            for extra in wrapped[1:]:
                out.append("  " + extra)
        return out

    def validate(self) -> None:
        super().validate()
        self.lines()

    def build(self) -> Any:
        self.validate()
        group = stacked_lines(self.lines(), "body", self.theme, self.theme.spacing.sm)
        group.item_count = len(normalize_items(self.param("items") or []))  # type: ignore[attr-defined]
        return self.clamp_to_content(group)


@text_component
class StepList(TextComponent):
    """Numbered steps for a short procedure."""

    component_id = "text.step_list"
    name = "Step List"
    subcategory = "list"
    tags = ["list", "steps", "procedure"]
    aliases = ["step-by-step list", "numbered steps"]
    parameters_schema = {
        "items": {"type": "array", "description": "Steps in order"}
    }

    def lines(self) -> List[str]:
        items = normalize_items(self.param("items", []) or [])
        budget = max(8, self.max_chars_for("body") - 4)
        out: List[str] = []
        for index, item in enumerate(items, start=1):
            wrapped = wrap_plain_text(item, budget)
            out.append(f"{index}. {wrapped[0]}")
            for extra in wrapped[1:]:
                out.append("   " + extra)
        return out

    def validate(self) -> None:
        super().validate()
        self.lines()

    def build(self) -> Any:
        self.validate()
        group = stacked_lines(self.lines(), "body", self.theme, self.theme.spacing.sm)
        return self.clamp_to_content(group)
