"""Transition recipes: scene and layout changes on the shared timeline.

These compose Part 2 motion wrappers when a fade or transform already exists.
Camera recipes require ``QuonitronMovingCameraScene``.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from quonitron_manim.motion.base import MotionError, MotionRecipe, import_manim, motion_component

DIRECTIONS = {
    "left": "LEFT",
    "right": "RIGHT",
    "up": "UP",
    "down": "DOWN",
    "LEFT": "LEFT",
    "RIGHT": "RIGHT",
    "UP": "UP",
    "DOWN": "DOWN",
}


class TransitionRecipe(MotionRecipe):
    """Motion recipe that typically has a source and a destination mobject."""

    category: str = "transition"
    subcategory: str = "simple"
    version: str = "0.4.0"
    needs_moving_camera: bool = False
    requires_source_dest: bool = True
    hides_content: bool = False
    related: List[str] = [
        "design.theme.quonitron_dark",
        "timeline.shared",
        "motion.appearance.fade_in",
    ]

    def direction_name(self) -> str:
        raw = str(self.params.get("direction", "LEFT"))
        if raw not in DIRECTIONS:
            raise MotionError(
                f"Unknown direction {raw!r}. Use one of {sorted(set(DIRECTIONS.values()))}"
            )
        return DIRECTIONS[raw]

    def vector(self, manim_mod, *, axis_only: Optional[str] = None):
        name = self.direction_name()
        unit = getattr(manim_mod, name)
        width = float(self.theme.frame_width)
        height = float(self.theme.frame_height)
        if name in {"LEFT", "RIGHT"}:
            return unit * (width + 0.4)
        return unit * (height + 0.4)

    def require_camera(self, scene: Any) -> Any:
        if scene is None or not hasattr(scene, "camera"):
            raise MotionError(
                f"{self.component_id} needs a live Scene with a camera"
            )
        frame = getattr(scene.camera, "frame", None)
        if frame is None:
            raise MotionError(
                f"{self.component_id} requires QuonitronMovingCameraScene "
                "(manim.MovingCameraScene). A plain Scene has no camera.frame."
            )
        return frame

    def validate(self) -> None:
        super().validate()
        if "direction" in self.params:
            self.direction_name()
        delay = self.params.get("delay")
        if delay is not None and float(delay) < 0:
            raise MotionError("delay must be >= 0")

    @classmethod
    def catalog_dict(cls) -> Dict[str, Any]:
        data = super().catalog_dict()
        data["category"] = "transition"
        extra = {
            "direction": {
                "type": "string",
                "description": "LEFT, RIGHT, UP, or DOWN where relevant",
                "enum": ["LEFT", "RIGHT", "UP", "DOWN"],
            },
            "delay": {
                "type": "number",
                "description": "Seconds to wait before the transition plays",
                "default": 0,
                "minimum": 0,
            },
        }
        params = data.setdefault("parameters", {})
        for key, spec in extra.items():
            params.setdefault(key, spec)
        return data


transition_component = motion_component
