"""Object-continuity transitions. These wrap Part 2 transform recipes."""

from __future__ import annotations

from typing import Any

from quonitron_manim.motion.base import MotionError, import_manim
from quonitron_manim.motion.position import MoveToMotion
from quonitron_manim.motion.transform import (
    FadeTransformMotion,
    ReplacementTransformMotion,
    TransformMatchingShapesMotion,
    TransformMotion,
)
from quonitron_manim.transitions.base import TransitionRecipe, transition_component


def _pair(targets):
    if len(targets) < 2:
        raise MotionError("continuity transitions need source and destination mobjects")
    return targets[0], targets[1]


@transition_component
class MorphTransition(TransitionRecipe):
    """Morph source into destination with Manim Transform (shared points)."""

    component_id = "transition.continuity.morph"
    name = "Morph"
    subcategory = "continuity"
    manim_api = "Transform"
    tags = ["morph", "transform", "continuity"]
    aliases = ["transform one object into another", "morph supported shapes"]
    use_cases = ["A variable card becoming a source-code token"]
    related = [
        "motion.transform.transform",
        "design.theme.quonitron_dark",
        "timeline.shared",
    ]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        source, dest = _pair(targets)
        return TransformMotion(theme=self.theme, run_time=self.run_time()).animate(
            source, dest
        )


@transition_component
class MatchShapesTransition(TransitionRecipe):
    """Pair corresponding submobjects by shape across two layouts."""

    component_id = "transition.continuity.match_shapes"
    name = "Match Shapes"
    subcategory = "continuity"
    manim_api = "TransformMatchingShapes"
    tags = ["match", "correspondence", "layout"]
    aliases = ["match corresponding objects across layouts"]
    related = ["motion.transform.matching_shapes", "timeline.shared"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        source, dest = _pair(targets)
        return TransformMatchingShapesMotion(
            theme=self.theme, run_time=self.run_time()
        ).animate(source, dest)


@transition_component
class ReplaceTransition(TransitionRecipe):
    """Replace source with destination in the scene."""

    component_id = "transition.continuity.replace"
    name = "Replace Visual"
    subcategory = "continuity"
    manim_api = "ReplacementTransform"
    tags = ["replace", "continuity"]
    aliases = ["replace one visual with another"]
    related = ["motion.transform.replacement", "timeline.shared"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        source, dest = _pair(targets)
        return ReplacementTransformMotion(
            theme=self.theme, run_time=self.run_time()
        ).animate(source, dest)


@transition_component
class RoleShiftTransition(TransitionRecipe):
    """Move the source into the destination's place, then replace."""

    component_id = "transition.continuity.role_shift"
    name = "Role Shift"
    subcategory = "continuity"
    manim_api = "Succession"
    tags = ["role", "move", "continuity"]
    aliases = ["move an object into its next conceptual role"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        source, dest = _pair(targets)
        dest_center = dest.get_center()
        rt = self.run_time()
        move = source.animate(run_time=rt * 0.55).move_to(dest_center)
        replace = ReplacementTransformMotion(
            theme=self.theme, run_time=rt * 0.45
        ).animate(source, dest)
        return manim.Succession(move, replace)


@transition_component
class SimplifyToDetailTransition(TransitionRecipe):
    """Cross-fade transform from a simplified model to a richer diagram."""

    component_id = "transition.continuity.simplify_to_detail"
    name = "Simplify To Detail"
    subcategory = "continuity"
    manim_api = "FadeTransform"
    tags = ["detail", "model", "diagram"]
    aliases = [
        "transform a simple diagram into a more detailed diagram",
        "transition from a simplified model to a detailed model",
    ]
    related = ["motion.transform.fade_transform", "timeline.shared"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        source, dest = _pair(targets)
        return FadeTransformMotion(theme=self.theme, run_time=self.run_time()).animate(
            source, dest
        )


@transition_component
class CarryAnchorTransition(TransitionRecipe):
    """Keep a named anchor (label) while the rest of the layout changes."""

    component_id = "transition.continuity.carry_anchor"
    name = "Carry Anchor"
    subcategory = "continuity"
    manim_api = "AnimationGroup"
    tags = ["anchor", "label", "preserve"]
    aliases = ["preserve selected labels or visual anchors across changes"]
    required_targets = 2
    limitations = (
        "Pass (outgoing_group, incoming_group). The recipe does not auto-detect "
        "labels; keep the shared label as a separate mobject and omit it from the groups."
    )

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        outgoing, incoming = _pair(targets)
        rt = self.run_time()
        return manim.AnimationGroup(
            manim.FadeOut(outgoing, run_time=rt),
            manim.FadeIn(incoming, run_time=rt),
        )
