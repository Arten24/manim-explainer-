"""Position and path-following recipes."""

from __future__ import annotations

from typing import Any, Sequence

from quonitron_manim.motion.base import MotionError, MotionRecipe, import_manim, motion_component


def _as_point(value: Any) -> Sequence[float]:
    if value is None:
        raise MotionError("point/target is required")
    if len(value) < 2:
        raise MotionError("point must be [x, y] or [x, y, z]")
    coords = [float(value[0]), float(value[1]), float(value[2]) if len(value) > 2 else 0.0]
    return coords


@motion_component
class MoveToMotion(MotionRecipe):
    """Move a mobject so its center sits at a target point."""

    component_id = "motion.position.move_to"
    name = "Move To"
    subcategory = "position"
    manim_api = "mobject.animate.move_to"
    tags = ["move", "position", "translate"]
    aliases = ["move to a position"]
    parameters_schema = {
        "target": {"type": "array", "description": "World point [x, y, z]", "required": True}
    }

    def validate(self) -> None:
        super().validate()
        if "target" in self.params:
            _as_point(self.params["target"])

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        mob = self._require_targets(targets)[0]
        point = _as_point(kwargs.get("target", self.param("target")))
        return mob.animate(run_time=self.run_time()).move_to(point)


@motion_component
class ShiftMotion(MotionRecipe):
    """Shift horizontally or vertically by a vector."""

    component_id = "motion.position.shift"
    name = "Shift"
    subcategory = "position"
    manim_api = "mobject.animate.shift"
    tags = ["shift", "nudge", "translate"]
    aliases = ["shift horizontally", "shift vertically"]
    parameters_schema = {
        "vector": {
            "type": "array",
            "description": "Displacement [dx, dy, dz] in scene units",
            "required": True,
        }
    }

    def validate(self) -> None:
        super().validate()
        if "vector" in self.params:
            _as_point(self.params["vector"])

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        import_manim()
        mob = self._require_targets(targets)[0]
        vec = _as_point(kwargs.get("vector", self.param("vector")))
        return mob.animate(run_time=self.run_time()).shift(vec)


@motion_component
class MoveAlongPathMotion(MotionRecipe):
    """Move a mobject along a VMobject path."""

    component_id = "motion.position.move_along_path"
    name = "Move Along Path"
    subcategory = "position"
    manim_api = "MoveAlongPath"
    tags = ["path", "follow", "track"]
    aliases = ["follow a path", "move along a path"]
    required_targets = 2
    limitations = (
        "Second argument must be a VMobject path. Requires Manim MoveAlongPath."
    )

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        mob, path = self._require_targets(targets)[:2]
        return manim.MoveAlongPath(mob, path, **self.kwargs_common())


@motion_component
class FollowPathMotion(MoveAlongPathMotion):
    """Alias recipe for MoveAlongPath with a follower-oriented name."""

    component_id = "motion.position.follow_path"
    name = "Follow Path"
    aliases = ["follow path"]
    related = [
        "motion.position.move_along_path",
        "design.theme.quonitron_dark",
        "timeline.shared",
    ]


@motion_component
class MoveBetweenAnchorsMotion(MotionRecipe):
    """Walk a mobject through a list of anchor points in order."""

    component_id = "motion.position.move_between_anchors"
    name = "Move Between Anchors"
    subcategory = "position"
    manim_api = "Succession"
    tags = ["anchors", "waypoints", "path"]
    aliases = ["move between anchor points"]
    parameters_schema = {
        "anchors": {
            "type": "array",
            "description": "List of world points",
            "required": True,
        }
    }

    def validate(self) -> None:
        super().validate()
        anchors = self.params.get("anchors")
        if anchors is not None:
            if not isinstance(anchors, (list, tuple)) or len(anchors) < 2:
                raise MotionError("anchors must contain at least two points")
            for point in anchors:
                _as_point(point)

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        mob = self._require_targets(targets)[0]
        anchors = kwargs.get("anchors", self.param("anchors"))
        if not anchors:
            raise MotionError("anchors is required")
        slice_time = self.run_time() / max(1, len(anchors) - 1)
        steps = [mob.animate(run_time=slice_time).move_to(_as_point(p)) for p in anchors]
        return manim.Succession(*steps)


@motion_component
class MoveGroupMotion(MotionRecipe):
    """Shift a group so relative layout is preserved."""

    component_id = "motion.position.move_group"
    name = "Move Group"
    subcategory = "position"
    manim_api = "mobject.animate.shift"
    tags = ["group", "layout", "shift"]
    aliases = ["move a group"]
    parameters_schema = {
        "vector": {"type": "array", "description": "Group displacement", "required": True}
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        mob = self._require_targets(targets)[0]
        vec = _as_point(kwargs.get("vector", self.param("vector")))
        return mob.animate(run_time=self.run_time()).shift(vec)


@motion_component
class EnterFrameMotion(MotionRecipe):
    """Slide a mobject in from a frame edge."""

    component_id = "motion.position.enter_frame"
    name = "Enter Frame"
    subcategory = "position"
    manim_api = "FadeIn"
    tags = ["enter", "frame", "slide"]
    aliases = ["smoothly enter the frame"]
    parameters_schema = {
        "edge": {
            "type": "string",
            "description": "LEFT, RIGHT, UP, or DOWN",
            "default": "LEFT",
        }
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        edge = str(kwargs.get("edge", self.param("edge", "LEFT")))
        direction = getattr(manim, edge)
        extra = self.kwargs_common()
        extra["shift"] = direction * 1.4
        return manim.FadeIn(self._require_targets(targets)[0], **extra)


@motion_component
class ExitFrameMotion(MotionRecipe):
    """Slide a mobject out through a frame edge."""

    component_id = "motion.position.exit_frame"
    name = "Exit Frame"
    subcategory = "position"
    manim_api = "FadeOut"
    tags = ["exit", "frame", "slide"]
    aliases = ["smoothly exit the frame"]
    parameters_schema = {
        "edge": {"type": "string", "description": "LEFT, RIGHT, UP, or DOWN", "default": "DOWN"}
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        edge = str(kwargs.get("edge", self.param("edge", "DOWN")))
        extra = self.kwargs_common()
        extra["shift"] = getattr(manim, edge) * 1.4
        return manim.FadeOut(self._require_targets(targets)[0], **extra)


@motion_component
class TrackLabelMotion(MotionRecipe):
    """Keep a label next to a moving host via an updater (not a timed Animation)."""

    component_id = "motion.position.track_label"
    name = "Track Label"
    subcategory = "position"
    manim_api = "Mobject.add_updater"
    tags = ["label", "tracker", "updater"]
    aliases = ["move an object while updating a related label", "label tracking"]
    required_targets = 2
    limitations = (
        "Attaches an updater; it is not a finite Animation. Call attach() rather "
        "than expecting Scene.play to consume a run_time. Remove the updater when "
        "the host leaves the scene."
    )
    parameters_schema = {
        "buff": {"type": "number", "description": "Gap in scene units", "default": 0.2}
    }

    def attach(self, label: Any, host: Any, direction: Any = None) -> Any:
        self.validate()
        manim = import_manim()
        buff = float(self.param("buff", 0.2))
        edge = direction if direction is not None else manim.UP

        def _follow(mob: Any) -> None:
            mob.next_to(host, edge, buff=buff)

        label.add_updater(_follow)
        _follow(label)
        return label

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        label, host = self._require_targets(targets)[:2]
        return self.attach(label, host, kwargs.get("direction"))
