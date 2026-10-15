"""Camera transitions. Require manim.MovingCameraScene (camera.frame)."""

from __future__ import annotations

from typing import Any

from quonitron_manim.motion.base import import_manim
from quonitron_manim.transitions.base import TransitionRecipe, transition_component


@transition_component
class ZoomInTransition(TransitionRecipe):
    """Zoom the moving camera into a selected mobject."""

    component_id = "transition.camera.zoom_in"
    name = "Zoom In"
    subcategory = "camera"
    manim_api = "MovingCamera.frame.animate"
    tags = ["zoom", "camera", "focus"]
    aliases = ["zoom into a selected object"]
    needs_moving_camera = True
    requires_source_dest = False
    required_targets = 1
    parameters_schema = {
        "margin": {
            "type": "number",
            "default": 1.6,
            "description": "Frame width as a multiple of the target width",
            "minimum": 1.05,
        }
    }
    limitations = (
        "Requires QuonitronMovingCameraScene. Pass scene= via kwargs. "
        "Does not run on a plain Cairo Scene."
    )

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        scene = kwargs.get("scene")
        frame = self.require_camera(scene)
        mob = self._require_targets(targets)[0]
        margin = float(kwargs.get("margin", self.param("margin", 1.6)))
        width = max(float(mob.width) * margin, 3.5)
        # Keep a little headroom so captions in the safe margin still exist.
        return frame.animate(**self.kwargs_common()).move_to(mob.get_center()).set(width=width)


@transition_component
class ZoomOutTransition(TransitionRecipe):
    """Zoom out to a wider context (default: full QUONITRON frame width)."""

    component_id = "transition.camera.zoom_out"
    name = "Zoom Out"
    subcategory = "camera"
    manim_api = "MovingCamera.frame.animate"
    tags = ["zoom", "camera", "context"]
    aliases = ["zoom out to reveal context"]
    needs_moving_camera = True
    requires_source_dest = False
    required_targets = 0
    parameters_schema = {
        "width": {
            "type": "number",
            "description": "Target frame width in scene units",
            "default": 14.222,
        }
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        scene = kwargs.get("scene")
        frame = self.require_camera(scene)
        width = float(kwargs.get("width", self.param("width", self.theme.frame_width)))
        return frame.animate(**self.kwargs_common()).move_to([0, 0, 0]).set(width=width)


@transition_component
class PanTransition(TransitionRecipe):
    """Pan the camera so the target sits at frame center."""

    component_id = "transition.camera.pan"
    name = "Pan"
    subcategory = "camera"
    manim_api = "MovingCamera.frame.animate.move_to"
    tags = ["pan", "camera"]
    aliases = ["pan to another visual region", "move the camera between focal points"]
    needs_moving_camera = True
    requires_source_dest = False
    required_targets = 1

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        scene = kwargs.get("scene")
        frame = self.require_camera(scene)
        mob = self._require_targets(targets)[0]
        return frame.animate(**self.kwargs_common()).move_to(mob.get_center())


@transition_component
class ReframeTransition(TransitionRecipe):
    """Move and resize the frame while keeping theme safe margins in mind."""

    component_id = "transition.camera.reframe"
    name = "Reframe"
    subcategory = "camera"
    manim_api = "MovingCamera.frame.animate"
    tags = ["reframe", "camera", "safe-area"]
    aliases = ["reframe content while preserving safe margins"]
    needs_moving_camera = True
    requires_source_dest = False
    required_targets = 1
    parameters_schema = {
        "margin": {"type": "number", "default": 1.8, "minimum": 1.1}
    }

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        scene = kwargs.get("scene")
        frame = self.require_camera(scene)
        mob = self._require_targets(targets)[0]
        margin = float(self.param("margin", 1.8))
        width = max(float(mob.width) * margin, self.theme.spacing.safe_margin * 8)
        return frame.animate(**self.kwargs_common()).move_to(mob.get_center()).set(width=width)


@transition_component
class CloseUpToFullTransition(TransitionRecipe):
    """Restore a wide shot from a close-up (uses saved camera.frame state when present)."""

    component_id = "transition.camera.closeup_to_full"
    name = "Close-up To Full"
    subcategory = "camera"
    manim_api = "Restore"
    tags = ["zoom", "restore", "camera"]
    aliases = ["transition from a close-up to a full diagram", "focus on one object and then another"]
    needs_moving_camera = True
    requires_source_dest = False
    required_targets = 0
    limitations = (
        "If camera.frame was save_state()'d, Restore is used. Otherwise zooms to "
        "the default frame width."
    )

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        scene = kwargs.get("scene")
        frame = self.require_camera(scene)
        manim = import_manim()
        saved = getattr(frame, "saved_state", None)
        if saved is not None:
            try:
                return manim.Restore(frame)
            except Exception:
                pass
        return frame.animate(**self.kwargs_common()).move_to([0, 0, 0]).set(
            width=self.theme.frame_width
        )


def camera_available(scene: Any) -> bool:
    return bool(scene is not None and getattr(getattr(scene, "camera", None), "frame", None))
