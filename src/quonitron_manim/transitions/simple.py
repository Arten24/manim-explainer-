"""Simple layout transitions. Fade/cut compose Part 2 appearance recipes."""

from __future__ import annotations

from typing import Any

from quonitron_manim.motion.appearance import FadeInMotion, FadeOutMotion, GrowFromCenterMotion
from quonitron_manim.motion.base import MotionError, import_manim
from quonitron_manim.transitions.base import TransitionRecipe, transition_component


def _pair(targets):
    if len(targets) < 2:
        raise MotionError("this transition needs outgoing and incoming mobjects")
    return targets[0], targets[1]


@transition_component
class FadeTransition(TransitionRecipe):
    """Cross-fade: outgoing fades out while incoming fades in."""

    component_id = "transition.simple.fade"
    name = "Fade Transition"
    subcategory = "simple"
    manim_api = "AnimationGroup(FadeOut, FadeIn)"
    tags = ["fade", "crossfade", "simple"]
    aliases = ["fade in and fade out", "cross fade"]
    use_cases = ["Soft change when objects do not correspond"]
    hides_content = False

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        outgoing, incoming = _pair(targets)
        rt = self.run_time()
        manim = import_manim()
        return manim.AnimationGroup(
            FadeOutMotion(theme=self.theme, run_time=rt).animate(outgoing),
            FadeInMotion(theme=self.theme, run_time=rt).animate(incoming),
        )


@transition_component
class CutTransition(TransitionRecipe):
    """Near-instant swap. Use sparingly for a hard editorial cut."""

    component_id = "transition.simple.cut"
    name = "Clean Cut"
    subcategory = "simple"
    manim_api = "AnimationGroup"
    tags = ["cut", "hard", "instant"]
    aliases = ["clean cut", "hard cut"]
    use_cases = ["Chapter title after a recap, when continuity would feel false"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        outgoing, incoming = _pair(targets)
        manim = import_manim()
        rt = min(0.08, self.run_time())
        return manim.AnimationGroup(
            FadeOutMotion(theme=self.theme, run_time=rt).animate(outgoing),
            FadeInMotion(theme=self.theme, run_time=rt).animate(incoming),
        )


@transition_component
class SlideTransition(TransitionRecipe):
    """Outgoing and incoming slide together so the layout feels continuous."""

    component_id = "transition.simple.slide"
    name = "Slide Transition"
    subcategory = "simple"
    manim_api = "AnimationGroup"
    tags = ["slide", "directional", "layout"]
    aliases = ["slide transition"]
    parameters_schema = {
        "direction": {"type": "string", "default": "LEFT", "description": "Incoming arrives from the opposite edge"}
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        outgoing, incoming = _pair(targets)
        vec = self.vector(manim)
        incoming.shift(-vec)
        extra = self.kwargs_common()
        extra.pop("rate_func", None)
        return manim.AnimationGroup(
            outgoing.animate.shift(vec),
            incoming.animate.shift(vec),
            **extra,
        )


@transition_component
class WipeTransition(TransitionRecipe):
    """A theme-colored bar wipes across the frame. May hide captions briefly."""

    component_id = "transition.simple.wipe"
    name = "Wipe"
    subcategory = "simple"
    manim_api = "Succession"
    tags = ["wipe", "directional", "cover"]
    aliases = ["wipe from left", "wipe from right", "wipe from top", "wipe from bottom"]
    hides_content = True
    parameters_schema = {
        "direction": {"type": "string", "default": "LEFT", "description": "Direction the bar travels"}
    }
    limitations = (
        "Uses a full-frame rectangle, not a pixel shader. Overlapping subtitle "
        "cues are warned as potentially unreadable."
    )

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        outgoing, incoming = _pair(targets)
        vec = self.vector(manim)
        bar = manim.Rectangle(
            width=self.theme.frame_width + 0.5,
            height=self.theme.frame_height + 0.5,
            fill_color=self.theme.color("background"),
            fill_opacity=1.0,
            stroke_width=0,
        )
        bar.shift(-vec)
        rt = self.run_time()
        return manim.Succession(
            manim.FadeIn(bar, run_time=0.02),
            bar.animate(run_time=rt * 0.44).shift(vec),
            manim.AnimationGroup(
                FadeOutMotion(theme=self.theme, run_time=0.05).animate(outgoing),
                FadeInMotion(theme=self.theme, run_time=0.05).animate(incoming),
            ),
            bar.animate(run_time=rt * 0.44).shift(vec),
            manim.FadeOut(bar, run_time=0.02),
        )


@transition_component
class CoverTransition(TransitionRecipe):
    """Incoming slides over outgoing (cover)."""

    component_id = "transition.simple.cover"
    name = "Cover"
    subcategory = "simple"
    manim_api = "AnimationGroup"
    tags = ["cover", "slide", "overlay"]
    aliases = ["cover"]
    hides_content = True
    parameters_schema = {"direction": {"type": "string", "default": "RIGHT"}}

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        outgoing, incoming = _pair(targets)
        vec = self.vector(manim)
        incoming.shift(-vec)
        return incoming.animate(**self.kwargs_common()).shift(vec)


@transition_component
class UncoverTransition(TransitionRecipe):
    """Outgoing slides away, revealing incoming already in place."""

    component_id = "transition.simple.uncover"
    name = "Uncover"
    subcategory = "simple"
    manim_api = "mobject.animate.shift"
    tags = ["uncover", "reveal"]
    aliases = ["uncover"]
    parameters_schema = {"direction": {"type": "string", "default": "LEFT"}}

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        outgoing, _incoming = _pair(targets)
        vec = self.vector(manim)
        return outgoing.animate(**self.kwargs_common()).shift(vec)


@transition_component
class DirectionalRevealTransition(TransitionRecipe):
    """Incoming fades in from a direction; outgoing fades out the other way."""

    component_id = "transition.simple.directional_reveal"
    name = "Directional Reveal"
    subcategory = "simple"
    manim_api = "AnimationGroup"
    tags = ["reveal", "directional", "fade"]
    aliases = ["directional reveal"]
    parameters_schema = {"direction": {"type": "string", "default": "UP"}}

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        outgoing, incoming = _pair(targets)
        name = self.direction_name()
        incoming_shift = getattr(manim, name) * 0.35
        rt = self.run_time()
        return manim.AnimationGroup(
            FadeOutMotion(theme=self.theme, run_time=rt, shift=name).animate(outgoing),
            manim.FadeIn(incoming, shift=-incoming_shift, run_time=rt),
        )


@transition_component
class ShapeRevealTransition(TransitionRecipe):
    """Incoming grows from center while outgoing fades."""

    component_id = "transition.simple.shape_reveal"
    name = "Shape Reveal"
    subcategory = "simple"
    manim_api = "GrowFromCenter"
    tags = ["shape", "grow", "reveal"]
    aliases = ["shape-based reveal"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        outgoing, incoming = _pair(targets)
        rt = self.run_time()
        return manim.AnimationGroup(
            FadeOutMotion(theme=self.theme, run_time=rt).animate(outgoing),
            GrowFromCenterMotion(theme=self.theme, run_time=rt).animate(incoming),
        )


@transition_component
class SequentialRevealTransition(TransitionRecipe):
    """Staggered entrance of the incoming group's submobjects."""

    component_id = "transition.simple.sequential_reveal"
    name = "Sequential Reveal"
    subcategory = "simple"
    manim_api = "LaggedStart"
    tags = ["stagger", "group", "reveal"]
    aliases = ["sequential reveal", "group entrance"]
    requires_source_dest = False
    parameters_schema = {
        "lag_ratio": {"type": "number", "default": 0.2, "minimum": 0, "maximum": 1}
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        from quonitron_manim.motion.appearance import StaggeredRevealMotion

        if not targets:
            raise MotionError("sequential reveal needs incoming mobjects")
        lag = float(self.param("lag_ratio", 0.2))
        return StaggeredRevealMotion(
            theme=self.theme, run_time=self.run_time(), lag_ratio=lag
        ).animate(*targets)


@transition_component
class GroupSwapTransition(TransitionRecipe):
    """Controlled swap of two visual groups."""

    component_id = "transition.simple.group_swap"
    name = "Group Swap"
    subcategory = "simple"
    manim_api = "AnimationGroup"
    tags = ["group", "swap", "layout"]
    aliases = ["controlled transition between visual groups"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        outgoing, incoming = _pair(targets)
        rt = self.run_time()
        return manim.AnimationGroup(
            FadeOutMotion(theme=self.theme, run_time=rt).animate(outgoing),
            FadeInMotion(theme=self.theme, run_time=rt).animate(incoming),
        )
