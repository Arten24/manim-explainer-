"""Scene contracts used by later templates.

These classes intentionally avoid importing Manim so catalog QA and unit
tests can run without Cairo. Visual Scene subclasses will wrap
``manim.Scene`` in Part 1+.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from quonitron.design import Theme, get_theme


@dataclass
class SceneSpec:
    scene_id: str
    title: str
    duration_hint: float = 8.0
    component_ids: List[str] = field(default_factory=list)
    subtitle_scene_id: Optional[str] = None
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "title": self.title,
            "duration_hint": self.duration_hint,
            "component_ids": list(self.component_ids),
            "subtitle_scene_id": self.subtitle_scene_id,
            "notes": self.notes,
        }


class QuonitronScene:
    """Non-Manim scene shell that carries theme + spec."""

    def __init__(
        self,
        spec: SceneSpec,
        theme: Optional[Theme] = None,
    ) -> None:
        self.spec = spec
        self.theme = theme or get_theme()

    @property
    def background_color(self) -> str:
        return self.theme.color("background")
