"""Rotation and scaling recipes."""

from __future__ import annotations

from typing import Any

from quonitron_manim.motion.base import MotionError, MotionRecipe, import_manim, motion_component


@motion_component
class RotateMotion(MotionRecipe):
    """Rotate around the mobject center by an angle in radians."""

    component_id = "motion.rotation.rotate"
    name = "Rotate"
    subcategory = "rotation"
    manim_api = "Rotate"
    tags = ["rotate", "spin"]
    aliases = ["rotate"]
    parameters_schema = {
        "angle": {"type": "number", "description": "Radians", "default": 0.785398}
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        angle = float(kwargs.get("angle", self.param("angle", 0.785398)))
        extra = self.kwargs_common()
        extra["about_point"] = self._require_targets(targets)[0].get_center()
        return manim.Rotate(self._require_targets(targets)[0], angle=angle, **extra)


@motion_component
class RotateAroundMotion(MotionRecipe):
    """Rotate around a configurable world point."""

    component_id = "motion.rotation.rotate_around"
    name = "Rotate Around"
    subcategory = "rotation"
    manim_api = "Rotate"
    tags = ["rotate", "pivot", "about"]
    aliases = ["rotate around a configurable point"]
    parameters_schema = {
        "angle": {"type": "number", "default": 0.785398},
        "about_point": {"type": "array", "description": "Pivot [x, y, z]", "required": True},
    }

    def validate(self) -> None:
        super().validate()
        if "about_point" in self.params:
            pt = self.params["about_point"]
            if pt is None or len(pt) < 2:
                raise MotionError("about_point must be [x, y] or [x, y, z]")

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        angle = float(kwargs.get("angle", self.param("angle", 0.785398)))
        point = kwargs.get("about_point", self.param("about_point"))
        extra = self.kwargs_common()
        extra["about_point"] = point
        return manim.Rotate(self._require_targets(targets)[0], angle=angle, **extra)


@motion_component
class ScaleMotion(MotionRecipe):
    """Scale up or down about the mobject center."""

    component_id = "motion.scale.scale"
    name = "Scale"
    subcategory = "scale"
    manim_api = "mobject.animate.scale"
    tags = ["scale", "size"]
    aliases = ["scale up or down"]
    parameters_schema = {
        "factor": {"type": "number", "description": "Scale factor", "required": True}
    }

    def validate(self) -> None:
        super().validate()
        if "factor" in self.params and float(self.params["factor"]) <= 0:
            raise MotionError("factor must be positive")

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        factor = float(kwargs.get("factor", self.param("factor")))
        return self._require_targets(targets)[0].animate(run_time=self.run_time()).scale(factor)


@motion_component
class GrowShrinkMotion(MotionRecipe):
    """Scale up and return (there-and-back)."""

    component_id = "motion.scale.grow_shrink"
    name = "Grow and Shrink"
    subcategory = "scale"
    manim_api = "Indicate"
    tags = ["grow", "shrink", "pulse"]
    aliases = ["grow and shrink"]
    parameters_schema = {
        "scale_factor": {"type": "number", "default": 1.18, "minimum": 1.0}
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        extra = self.kwargs_common()
        extra["scale_factor"] = float(self.param("scale_factor", 1.18))
        extra["color"] = self.theme.color("text_primary")
        return manim.Indicate(self._require_targets(targets)[0], **extra)


@motion_component
class RotateAndMoveMotion(MotionRecipe):
    """Rotate while shifting — composed as an AnimationGroup."""

    component_id = "motion.rotation.rotate_and_move"
    name = "Rotate and Move"
    subcategory = "rotation"
    manim_api = "AnimationGroup"
    tags = ["rotate", "move", "compose"]
    aliases = ["rotate and move together"]
    parameters_schema = {
        "angle": {"type": "number", "default": 0.5},
        "vector": {"type": "array", "description": "Shift [dx, dy, dz]", "required": True},
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        mob = self._require_targets(targets)[0]
        angle = float(kwargs.get("angle", self.param("angle", 0.5)))
        vector = kwargs.get("vector", self.param("vector"))
        extra = self.kwargs_common()
        extra.pop("rate_func", None)
        return manim.AnimationGroup(
            manim.Rotate(mob, angle=angle, about_point=mob.get_center()),
            mob.animate.shift(vector),
            **extra,
        )
