"""Equations. MathTex when LaTeX is available, themed Text otherwise."""

from __future__ import annotations

from typing import Any

from quonitron_manim.components.text.base import TextComponent, text_component
from quonitron_manim.components.text.wrap import TextLayoutError
from quonitron_manim.core.text import themed_text


@text_component
class EquationText(TextComponent):
    """A single equation. Uses manim.MathTex, falling back to Text if LaTeX fails."""

    component_id = "text.equation"
    name = "Equation"
    subcategory = "math"
    tags = ["equation", "math", "tex"]
    aliases = ["mathematical expression", "equation"]
    use_cases = ["Show score as a named quantity without a full math lecture"]
    limitations = (
        "MathTex needs a LaTeX install. Without it the component renders the source as Text."
    )
    related = ["design.theme.quonitron_dark", "motion.appearance.write"]
    parameters_schema = {
        "tex": {
            "type": "string",
            "description": "TeX body, without surrounding $$",
            "default": "score = 10",
        },
        "color_role": {
            "type": "string",
            "description": "Palette role",
            "default": "equation",
        },
    }

    def validate(self) -> None:
        super().validate()
        if not str(self.param("tex", "")).strip():
            raise TextLayoutError("text.equation needs non-empty tex")

    def build(self) -> Any:
        self.validate()
        tex = str(self.param("tex")).strip()
        color = self.theme.color(str(self.param("color_role", "equation")))
        try:
            from manim import MathTex

            mob = MathTex(tex, color=color)
            self.used_mathtex = True
        except Exception:
            mob = themed_text(tex, "equation", self.theme)
            self.used_mathtex = False
        mob.used_mathtex = self.used_mathtex  # type: ignore[attr-defined]
        return self.clamp_to_content(mob)
