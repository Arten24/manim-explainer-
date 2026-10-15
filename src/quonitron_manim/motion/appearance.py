"""Appearance and disappearance recipes (Manim 0.22 creation/fading/growing)."""

from __future__ import annotations

from typing import Any

from quonitron_manim.motion.base import MotionRecipe, import_manim, motion_component


@motion_component
class FadeInMotion(MotionRecipe):
    """Fade a mobject in, optionally shifting from a direction."""

    component_id = "motion.appearance.fade_in"
    name = "Fade In"
    subcategory = "appearance"
    manim_api = "FadeIn"
    tags = ["fade", "appear", "entrance"]
    aliases = ["fadein", "appear fade"]
    use_cases = ["Bring a diagram into the scene without drawing its path"]
    parameters_schema = {
        "shift": {"type": "string", "description": "Optional direction name: UP, DOWN, LEFT, RIGHT"}
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        mob = self._require_targets(targets)[0]
        shift = kwargs.get("shift", self.param("shift"))
        extra = self.kwargs_common()
        if shift:
            extra["shift"] = getattr(manim, str(shift)) * 0.25
        return manim.FadeIn(mob, **extra)


@motion_component
class FadeOutMotion(MotionRecipe):
    """Fade a mobject out, optionally shifting off-frame."""

    component_id = "motion.appearance.fade_out"
    name = "Fade Out"
    subcategory = "appearance"
    manim_api = "FadeOut"
    tags = ["fade", "exit", "disappear"]
    aliases = ["fadeout"]
    use_cases = ["Remove a title before the educational content"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        mob = self._require_targets(targets)[0]
        extra = self.kwargs_common()
        shift = kwargs.get("shift", self.param("shift"))
        if shift:
            extra["shift"] = getattr(manim, str(shift)) * 0.25
        return manim.FadeOut(mob, **extra)


@motion_component
class CreateMotion(MotionRecipe):
    """Draw a VMobject along its path (Manim Create, not the deprecated ShowCreation)."""

    component_id = "motion.appearance.create"
    name = "Create"
    subcategory = "appearance"
    manim_api = "Create"
    tags = ["create", "draw", "stroke"]
    aliases = ["show creation", "draw path"]
    use_cases = ["Draw a box, arrow, or path into existence"]
    limitations = (
        "Uses manim.Create (ShowCreation was removed). Works best on VMobjects."
    )

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        return manim.Create(self._require_targets(targets)[0], **self.kwargs_common())


@motion_component
class UncreateMotion(MotionRecipe):
    """Reverse of Create."""

    component_id = "motion.appearance.uncreate"
    name = "Uncreate"
    subcategory = "appearance"
    manim_api = "Uncreate"
    tags = ["uncreate", "erase"]
    aliases = ["erase path"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        return manim.Uncreate(self._require_targets(targets)[0], **self.kwargs_common())


@motion_component
class WriteMotion(MotionRecipe):
    """Write text or a VMobject as if it were being inscribed."""

    component_id = "motion.appearance.write"
    name = "Write"
    subcategory = "appearance"
    manim_api = "Write"
    tags = ["write", "text", "inscription"]
    aliases = ["handwrite"]
    use_cases = ["Introduce a variable name or heading"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        return manim.Write(self._require_targets(targets)[0], **self.kwargs_common())


@motion_component
class DrawBorderThenFillMotion(MotionRecipe):
    """Stroke the outline, then fill."""

    component_id = "motion.appearance.draw_border_then_fill"
    name = "Draw Border Then Fill"
    subcategory = "appearance"
    manim_api = "DrawBorderThenFill"
    tags = ["border", "fill", "draw"]
    aliases = ["draw border around"]
    use_cases = ["Reveal a variable card by outlining it first"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        return manim.DrawBorderThenFill(
            self._require_targets(targets)[0], **self.kwargs_common()
        )


@motion_component
class GrowFromCenterMotion(MotionRecipe):
    """Grow a mobject from its center."""

    component_id = "motion.appearance.grow_from_center"
    name = "Grow From Center"
    subcategory = "appearance"
    manim_api = "GrowFromCenter"
    tags = ["grow", "scale", "entrance"]
    aliases = ["pop in"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        return manim.GrowFromCenter(
            self._require_targets(targets)[0], **self.kwargs_common()
        )


@motion_component
class GrowFromPointMotion(MotionRecipe):
    """Grow a mobject from a world-space point."""

    component_id = "motion.appearance.grow_from_point"
    name = "Grow From Point"
    subcategory = "appearance"
    manim_api = "GrowFromPoint"
    tags = ["grow", "point", "origin"]
    aliases = ["grow from a point"]
    parameters_schema = {
        "point": {
            "type": "array",
            "description": "World coordinates [x, y, z]",
            "default": [0, 0, 0],
        }
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        point = kwargs.get("point", self.param("point", [0, 0, 0]))
        return manim.GrowFromPoint(
            self._require_targets(targets)[0], point, **self.kwargs_common()
        )


@motion_component
class SmoothEntranceMotion(MotionRecipe):
    """Fade in with a small upward settle. Default Part 2 entrance."""

    component_id = "motion.appearance.smooth_entrance"
    name = "Smooth Entrance"
    subcategory = "appearance"
    manim_api = "FadeIn"
    tags = ["entrance", "smooth", "fade"]
    aliases = ["soft enter"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        extra = self.kwargs_common()
        extra["shift"] = manim.DOWN * 0.18
        return manim.FadeIn(self._require_targets(targets)[0], **extra)


@motion_component
class SmoothExitMotion(MotionRecipe):
    """Fade out with a small downward drift."""

    component_id = "motion.appearance.smooth_exit"
    name = "Smooth Exit"
    subcategory = "appearance"
    manim_api = "FadeOut"
    tags = ["exit", "smooth", "fade"]
    aliases = ["soft leave"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        extra = self.kwargs_common()
        extra["shift"] = manim.DOWN * 0.12
        return manim.FadeOut(self._require_targets(targets)[0], **extra)


@motion_component
class StaggeredRevealMotion(MotionRecipe):
    """Lagged fade-in of several mobjects, preserving order."""

    component_id = "motion.appearance.staggered_reveal"
    name = "Staggered Reveal"
    subcategory = "appearance"
    manim_api = "LaggedStart"
    tags = ["stagger", "group", "reveal", "lag"]
    aliases = ["reveal group", "ordered reveal"]
    required_targets = 1
    parameters_schema = {
        "lag_ratio": {
            "type": "number",
            "description": "0 = together, 1 = fully sequential",
            "default": 0.2,
            "minimum": 0,
            "maximum": 1,
        }
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        from quonitron_manim.motion.base import MotionError

        if not targets:
            raise MotionError("staggered reveal needs at least one mobject")
        lag = float(kwargs.get("lag_ratio", self.param("lag_ratio", 0.2)))
        fades = [manim.FadeIn(mob, shift=manim.DOWN * 0.1) for mob in targets]
        extra = self.kwargs_common()
        extra.pop("rate_func", None)
        return manim.LaggedStart(*fades, lag_ratio=lag, **extra)
