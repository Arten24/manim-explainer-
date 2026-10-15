"""Small geometric and numeric motion utilities."""

from __future__ import annotations

from typing import Any

from quonitron_manim.motion.base import MotionError, MotionRecipe, import_manim, motion_component


@motion_component
class CreateLineMotion(MotionRecipe):
    """Create (draw) a line or arrow VMobject."""

    component_id = "motion.util.create_line"
    name = "Create Line"
    subcategory = "utility"
    manim_api = "Create"
    tags = ["line", "arrow", "draw"]
    aliases = ["animated line creation"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        return manim.Create(self._require_targets(targets)[0], **self.kwargs_common())


@motion_component
class MoveArrowMotion(MotionRecipe):
    """Shift an arrow, typically from a name toward a value."""

    component_id = "motion.util.move_arrow"
    name = "Move Arrow"
    subcategory = "utility"
    manim_api = "mobject.animate.shift"
    tags = ["arrow", "move"]
    aliases = ["arrow movement"]
    parameters_schema = {
        "vector": {"type": "array", "description": "Displacement", "required": True}
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        vec = kwargs.get("vector", self.param("vector"))
        if vec is None:
            raise MotionError("vector is required")
        return self._require_targets(targets)[0].animate(run_time=self.run_time()).shift(vec)


@motion_component
class DotAlongLineMotion(MotionRecipe):
    """Move a dot along a line or path."""

    component_id = "motion.util.dot_along_line"
    name = "Dot Along Line"
    subcategory = "utility"
    manim_api = "MoveAlongPath"
    tags = ["dot", "line", "trace"]
    aliases = ["dot movement along a line", "endpoint tracking"]
    required_targets = 2

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        dot, path = self._require_targets(targets)[:2]
        return manim.MoveAlongPath(dot, path, **self.kwargs_common())


@motion_component
class TracedPathMotion(MotionRecipe):
    """Return a TracedPath mobject that follows another mobject.

    This is a mobject constructor, not a finite Animation. Call build_tracer().
    """

    component_id = "motion.util.traced_path"
    name = "Traced Path"
    subcategory = "utility"
    manim_api = "TracedPath"
    tags = ["trace", "path"]
    aliases = ["simple path tracing"]
    required_targets = 1
    limitations = (
        "Returns a TracedPath mobject. Add it to the scene, then animate the "
        "host. It is not passed to Scene.play as an Animation."
    )

    def build_tracer(self, host: Any) -> Any:
        manim = import_manim()
        return manim.TracedPath(host.get_center, stroke_color=self.theme.color("accent"))

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        return self.build_tracer(self._require_targets(targets)[0])


@motion_component
class ChangingDecimalMotion(MotionRecipe):
    """Animate a DecimalNumber to a new value."""

    component_id = "motion.util.changing_decimal"
    name = "Changing Decimal"
    subcategory = "utility"
    manim_api = "ChangeDecimalToValue"
    tags = ["number", "counter", "decimal"]
    aliases = ["smooth counter updates"]
    parameters_schema = {
        "value": {"type": "number", "description": "Target value", "required": True}
    }

    def validate(self) -> None:
        super().validate()
        if "value" in self.params:
            float(self.params["value"])

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        mob = self._require_targets(targets)[0]
        value = float(kwargs.get("value", self.param("value")))
        return manim.ChangeDecimalToValue(mob, value, **self.kwargs_common())
