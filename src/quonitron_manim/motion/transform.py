"""Transform and property-interpolation recipes."""

from __future__ import annotations

from typing import Any

from quonitron_manim.motion.base import MotionError, MotionRecipe, import_manim, motion_component


@motion_component
class TransformMotion(MotionRecipe):
    """Morph source into the shape of target; source remains the on-scene mobject."""

    component_id = "motion.transform.transform"
    name = "Transform"
    subcategory = "transform"
    manim_api = "Transform"
    tags = ["transform", "morph"]
    aliases = ["transform one object into another"]
    required_targets = 2

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        source, dest = self._require_targets(targets)[:2]
        return manim.Transform(source, dest, **self.kwargs_common())


@motion_component
class ReplacementTransformMotion(MotionRecipe):
    """Replace source with target in the scene."""

    component_id = "motion.transform.replacement"
    name = "Replacement Transform"
    subcategory = "transform"
    manim_api = "ReplacementTransform"
    tags = ["replace", "transform", "value"]
    aliases = ["replacement transform"]
    required_targets = 2
    use_cases = ["Swap a stored value for a new one inside a variable card"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        source, dest = self._require_targets(targets)[:2]
        return manim.ReplacementTransform(source, dest, **self.kwargs_common())


@motion_component
class TransformMatchingShapesMotion(MotionRecipe):
    """Match submobjects by shape and transform them pairwise."""

    component_id = "motion.transform.matching_shapes"
    name = "Transform Matching Shapes"
    subcategory = "transform"
    manim_api = "TransformMatchingShapes"
    tags = ["matching", "transform", "text"]
    aliases = ["transform matching objects", "transform text"]
    required_targets = 2

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        source, dest = self._require_targets(targets)[:2]
        return manim.TransformMatchingShapes(source, dest, **self.kwargs_common())


@motion_component
class TransformMatchingTexMotion(MotionRecipe):
    """Match TeX parts by tex string. Requires a LaTeX installation."""

    component_id = "motion.transform.matching_tex"
    name = "Transform Matching Tex"
    subcategory = "transform"
    manim_api = "TransformMatchingTex"
    tags = ["tex", "formula", "transform"]
    aliases = ["transform mathematical expressions"]
    required_targets = 2
    limitations = (
        "Requires LaTeX. Not used in the Part 2 demo. Fails if tex_template "
        "cannot compile."
    )

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        source, dest = self._require_targets(targets)[:2]
        return manim.TransformMatchingTex(source, dest, **self.kwargs_common())


@motion_component
class FadeTransformMotion(MotionRecipe):
    """Cross-fade transform, useful when topology differs."""

    component_id = "motion.transform.fade_transform"
    name = "Fade Transform"
    subcategory = "transform"
    manim_api = "FadeTransform"
    tags = ["fade", "morph"]
    aliases = ["object-to-object transition"]
    required_targets = 2

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        source, dest = self._require_targets(targets)[:2]
        return manim.FadeTransform(source, dest, **self.kwargs_common())


@motion_component
class MorphPropertyMotion(MotionRecipe):
    """Interpolate color, opacity, and/or scale on one mobject."""

    component_id = "motion.transform.morph_property"
    name = "Morph Property"
    subcategory = "transform"
    manim_api = "mobject.animate"
    tags = ["color", "opacity", "scale", "interpolate"]
    aliases = [
        "animate changes in object properties",
        "interpolate position, scale, color, and opacity",
    ]
    parameters_schema = {
        "color": {"type": "string", "description": "Theme color role or hex"},
        "opacity": {"type": "number", "minimum": 0, "maximum": 1},
        "scale": {"type": "number", "description": "Scale factor relative to current size"},
        "target": {"type": "array", "description": "Optional destination point"},
    }

    def validate(self) -> None:
        super().validate()
        if self.param("opacity") is not None:
            op = float(self.param("opacity"))
            if op < 0 or op > 1:
                raise MotionError("opacity must be between 0 and 1")
        if self.param("scale") is not None and float(self.param("scale")) <= 0:
            raise MotionError("scale must be positive")

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        from quonitron_manim.design import get_theme

        mob = self._require_targets(targets)[0]
        builder = mob.animate(run_time=self.run_time())
        color = kwargs.get("color", self.param("color"))
        if color:
            if isinstance(color, str) and not color.startswith("#"):
                color = get_theme().color(color) if hasattr(self.theme, "color") else color
                try:
                    color = self.theme.color(kwargs.get("color", self.param("color")))
                except ValueError:
                    color = kwargs.get("color", self.param("color"))
            builder = builder.set_color(color)
        if self.param("opacity") is not None:
            builder = builder.set_opacity(float(self.param("opacity")))
        if self.param("scale") is not None:
            builder = builder.scale(float(self.param("scale")))
        if self.param("target") is not None:
            builder = builder.move_to(self.param("target"))
        return builder
