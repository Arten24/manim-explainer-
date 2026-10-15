"""Group, sequence, and wait recipes."""

from __future__ import annotations

from typing import Any, List

from quonitron_manim.motion.base import MotionError, MotionRecipe, import_manim, motion_component


@motion_component
class SequentialMotion(MotionRecipe):
    """Play animations one after another (Manim Succession)."""

    component_id = "motion.group.sequential"
    name = "Sequential"
    subcategory = "group"
    manim_api = "Succession"
    tags = ["sequence", "succession", "timeline"]
    aliases = ["sequential animation"]
    required_targets = 0
    limitations = (
        "Pass already-built Animation objects to animate(), not mobjects."
    )

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        if len(targets) < 2:
            raise MotionError("sequential motion needs at least two animations")
        extra = self.kwargs_common()
        extra.pop("rate_func", None)
        return manim.Succession(*targets, **extra)


@motion_component
class ParallelMotion(MotionRecipe):
    """Play animations together (Manim AnimationGroup)."""

    component_id = "motion.group.parallel"
    name = "Parallel"
    subcategory = "group"
    manim_api = "AnimationGroup"
    tags = ["parallel", "together", "group"]
    aliases = ["parallel animation", "coordinated object movement"]
    required_targets = 0

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        if not targets:
            raise MotionError("parallel motion needs at least one animation")
        extra = self.kwargs_common()
        extra.pop("rate_func", None)
        return manim.AnimationGroup(*targets, **extra)


@motion_component
class StaggeredGroupMotion(MotionRecipe):
    """LaggedStart over supplied animations."""

    component_id = "motion.group.staggered"
    name = "Staggered Group"
    subcategory = "group"
    manim_api = "LaggedStart"
    tags = ["stagger", "lag", "group"]
    aliases = ["staggered groups"]
    required_targets = 0
    parameters_schema = {
        "lag_ratio": {"type": "number", "default": 0.25, "minimum": 0, "maximum": 1}
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        if not targets:
            raise MotionError("staggered group needs at least one animation")
        lag = float(kwargs.get("lag_ratio", self.param("lag_ratio", 0.25)))
        extra = self.kwargs_common()
        extra.pop("rate_func", None)
        return manim.LaggedStart(*targets, lag_ratio=lag, **extra)


@motion_component
class WaitMotion(MotionRecipe):
    """Hold the frame. Encodes an explicit pause on the shared timeline."""

    component_id = "motion.timing.wait"
    name = "Wait"
    subcategory = "timing"
    category = "motion"
    manim_api = "Wait"
    tags = ["wait", "pause", "gap", "hold"]
    aliases = ["pause", "gap"]
    required_targets = 0
    use_cases = ["Leave a breath between an explanation and the next visual"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        return manim.Wait(self.run_time())


def group_entrance(mobjects: List[Any], **params: Any) -> Any:
    """Convenience: staggered fade-in of a list of mobjects."""
    from quonitron_manim.motion.appearance import StaggeredRevealMotion

    return StaggeredRevealMotion(**params).animate(*mobjects)


def group_exit(mobjects: List[Any], **params: Any) -> Any:
    """Convenience: parallel fade-out."""
    manim = import_manim()
    anims = [manim.FadeOut(mob) for mob in mobjects]
    extra_rt = params.get("run_time", 0.4)
    return manim.AnimationGroup(*anims, run_time=extra_rt)
