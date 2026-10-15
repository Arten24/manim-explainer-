"""Attention and emphasis recipes."""

from __future__ import annotations

from typing import Any

from quonitron_manim.motion.base import MotionRecipe, import_manim, motion_component


@motion_component
class IndicateMotion(MotionRecipe):
    """Scale-pulse a mobject to draw attention."""

    component_id = "motion.emphasis.indicate"
    name = "Indicate"
    subcategory = "emphasis"
    manim_api = "Indicate"
    tags = ["indicate", "pulse", "attention"]
    aliases = ["emphasize a label or formula"]
    parameters_schema = {
        "scale_factor": {"type": "number", "default": 1.15, "minimum": 1.0}
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        extra = self.kwargs_common()
        extra["scale_factor"] = float(
            kwargs.get("scale_factor", self.param("scale_factor", 1.15))
        )
        extra["color"] = self.theme.color("accent")
        return manim.Indicate(self._require_targets(targets)[0], **extra)


@motion_component
class CircumscribeMotion(MotionRecipe):
    """Draw a temporary rectangle or circle around a mobject."""

    component_id = "motion.emphasis.circumscribe"
    name = "Circumscribe"
    subcategory = "emphasis"
    manim_api = "Circumscribe"
    tags = ["circumscribe", "outline", "attention"]
    aliases = ["draw border around an object"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        extra = self.kwargs_common()
        extra["color"] = self.theme.color("accent")
        extra["fade_out"] = True
        return manim.Circumscribe(self._require_targets(targets)[0], **extra)


@motion_component
class FlashMotion(MotionRecipe):
    """Radial flash at a point, defaulting to the mobject center."""

    component_id = "motion.emphasis.flash"
    name = "Flash"
    subcategory = "emphasis"
    manim_api = "Flash"
    tags = ["flash", "spark", "attention"]
    aliases = ["flash"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        mob = self._require_targets(targets)[0]
        extra = self.kwargs_common()
        extra["color"] = self.theme.color("highlight")
        extra["line_length"] = 0.35
        extra["num_lines"] = 8
        point = kwargs.get("point", mob.get_center())
        return manim.Flash(point, **extra)


@motion_component
class WiggleMotion(MotionRecipe):
    """Wiggle in place."""

    component_id = "motion.emphasis.wiggle"
    name = "Wiggle"
    subcategory = "emphasis"
    manim_api = "Wiggle"
    tags = ["wiggle", "shake"]
    aliases = ["wiggle"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        return manim.Wiggle(self._require_targets(targets)[0], **self.kwargs_common())


@motion_component
class PulseMotion(MotionRecipe):
    """There-and-back scale emphasis."""

    component_id = "motion.emphasis.pulse"
    name = "Pulse"
    subcategory = "emphasis"
    manim_api = "Indicate"
    tags = ["pulse", "scale", "emphasis"]
    aliases = ["pulse or scale emphasis"]
    parameters_schema = {
        "scale_factor": {"type": "number", "default": 1.2, "minimum": 1.0}
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        extra = self.kwargs_common()
        extra["scale_factor"] = float(self.param("scale_factor", 1.2))
        extra["color"] = self.theme.color("highlight")
        return manim.Indicate(self._require_targets(targets)[0], **extra)


@motion_component
class FocusOnMotion(MotionRecipe):
    """Camera-like focus pulse toward a mobject."""

    component_id = "motion.emphasis.focus_on"
    name = "Focus On"
    subcategory = "emphasis"
    manim_api = "FocusOn"
    tags = ["focus", "attention"]
    aliases = ["focus attention"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        extra = self.kwargs_common()
        extra["color"] = self.theme.color("accent")
        return manim.FocusOn(self._require_targets(targets)[0], **extra)


@motion_component
class HighlightLineMotion(MotionRecipe):
    """Emphasize one mobject (a code line, formula, or label) with Indicate."""

    component_id = "motion.emphasis.highlight_line"
    name = "Highlight Line"
    subcategory = "emphasis"
    manim_api = "Indicate"
    tags = ["code", "highlight", "line"]
    aliases = ["highlight a line of code"]
    limitations = (
        "Operates on a mobject you pass in. It does not parse source files. "
        "For a code block, pass the submobject that represents the line."
    )

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        extra = self.kwargs_common()
        extra["color"] = self.theme.color("highlight")
        extra["scale_factor"] = 1.08
        return manim.Indicate(self._require_targets(targets)[0], **extra)


@motion_component
class FocusSetMotion(MotionRecipe):
    """Keep the first mobject full opacity; fade the rest to a muted opacity."""

    component_id = "motion.emphasis.focus_set"
    name = "Focus Set"
    subcategory = "emphasis"
    manim_api = "AnimationGroup"
    tags = ["focus", "deemphasize", "opacity"]
    aliases = ["focus attention on one object while de-emphasizing others"]
    required_targets = 2
    parameters_schema = {
        "muted_opacity": {"type": "number", "default": 0.22, "minimum": 0, "maximum": 1}
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        focus, *others = self._require_targets(targets)
        muted = float(kwargs.get("muted_opacity", self.param("muted_opacity", 0.22)))
        anims = [manim.Indicate(focus, color=self.theme.color("accent"), scale_factor=1.08)]
        for mob in others:
            anims.append(mob.animate.set_opacity(muted))
        extra = self.kwargs_common()
        extra.pop("rate_func", None)
        return manim.AnimationGroup(*anims, **extra)
