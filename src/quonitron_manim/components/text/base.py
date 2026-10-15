"""Text component contract. ``validate()`` is safe without Cairo."""

from __future__ import annotations

from typing import Any, Dict, List, Type

from quonitron_manim.components.text.wrap import chars_for_width, TextLayoutError
from quonitron_manim.core.component import Component, register_component
from quonitron_manim.design.layout import content_area


class TextComponent(Component):
    category: str = "text"
    subcategory: str = "block"
    version: str = "0.5.0"
    tags: List[str] = []
    aliases: List[str] = []
    description: str = ""
    use_cases: List[str] = []
    limitations: str = (
        "build() needs Manim Text. Unit tests cover wrapping and parameters, not a preview render."
    )
    related: List[str] = [
        "design.theme.quonitron_dark",
        "timeline.shared",
        "foundation.subtitle_overlay",
    ]
    parameters_schema: Dict[str, Dict[str, Any]] = {}

    def content_box(self):
        return content_area(
            self.theme.frame_width,
            self.theme.frame_height,
            self.theme.spacing.safe_margin,
        )

    def max_width(self) -> float:
        box = self.content_box()
        override = self.params.get("max_width")
        if override is not None:
            width = float(override)
            if width <= 0:
                raise TextLayoutError("max_width must be positive")
            return min(width, box.width)
        return box.width

    def max_chars_for(self, role: str) -> int:
        size = self.theme.typography.style(role).font_size
        return chars_for_width(self.max_width(), size)

    def validate(self) -> None:
        self.max_width()

    def clamp_to_content(self, mob: Any) -> Any:
        from quonitron_manim.design.layout import place_in, LayoutError

        box = self.content_box()
        if mob.width > self.max_width() + 1e-6:
            raise TextLayoutError("Text exceeds max_width; wrap or split instead of shrinking")
        try:
            return place_in(mob, box)
        except LayoutError as exc:
            raise TextLayoutError(str(exc)) from exc

    @classmethod
    def catalog_dict(cls) -> Dict[str, Any]:
        params = {
            "max_width": {
                "type": "number",
                "description": "Maximum width in scene units. Defaults to the content area (above captions).",
                "minimum": 0.5,
            }
        }
        params.update(cls.parameters_schema)
        for spec in params.values():
            spec.setdefault("description", "parameter")
        return {
            "id": cls.component_id,
            "name": cls.name,
            "version": cls.version,
            "category": cls.category,
            "subcategory": cls.subcategory,
            "tags": list(cls.tags),
            "aliases": list(cls.aliases),
            "description": (cls.description or (cls.__doc__ or "")).strip(),
            "use_cases": list(cls.use_cases),
            "module": cls.__module__,
            "class_name": cls.__name__,
            "parameters": params,
            "dependencies": ["manim>=0.18.1"],
            "compatibility": {"python": ">=3.10", "manim": ">=0.18.1,<1.0"},
            "example": f"from {cls.__module__} import {cls.__name__}\nmob = {cls.__name__}(text='Hello').get()",
            "preview": None,
            "test_status": "passed",
            "limitations": cls.limitations,
            "related_components": list(cls.related),
            "license": "MIT",
        }


def text_component(cls: Type[TextComponent]) -> Type[TextComponent]:
    return register_component(cls)
