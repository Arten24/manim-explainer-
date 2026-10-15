"""Motion recipes: theme-aware wrappers around Manim Community animations.

A recipe is a Component that produces an Animation, not a decorative
mobject. ``validate()`` is safe without Cairo. ``animate()`` imports Manim
lazily and raises ImportError when the renderer stack is missing.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Type

from quonitron_manim.core.component import Component, register_component
from quonitron_manim.design.motion import EASING_ALIASES


class MotionError(ValueError):
    """Invalid motion parameters or a missing target."""


class MotionRecipe(Component):
    """Base class for Part 2 motion catalog entries."""

    category: str = "motion"
    subcategory: str = "appearance"
    version: str = "0.3.0"
    manim_api: str = ""
    tags: List[str] = []
    aliases: List[str] = []
    description: str = ""
    use_cases: List[str] = []
    limitations: str = (
        "Requires Manim Community Edition to build the Animation. "
        "Unit tests cover parameter validation only."
    )
    example: str = ""
    related: List[str] = ["design.theme.quonitron_dark", "timeline.shared"]
    parameters_schema: Dict[str, Dict[str, Any]] = {}
    required_targets: int = 1

    def run_time(self) -> float:
        if "run_time" in self.params and self.params["run_time"] is not None:
            try:
                value = float(self.params["run_time"])
            except (TypeError, ValueError) as exc:
                raise MotionError("run_time must be a number") from exc
        else:
            speed = str(self.params.get("speed", "normal"))
            try:
                value = self.theme.duration(speed)
            except ValueError as exc:
                raise MotionError(str(exc)) from exc
        if value <= 0:
            raise MotionError("run_time must be positive")
        return value

    def easing_name(self) -> str:
        return str(self.params.get("easing", self.theme.motion.easing_default))

    def validate(self) -> None:
        self.run_time()
        name = self.easing_name()
        if name not in EASING_ALIASES and name not in EASING_ALIASES.values():
            raise MotionError(
                f"Unknown easing {name!r}. Known: {sorted(EASING_ALIASES)}"
            )
        lag = self.params.get("lag_ratio")
        if lag is not None:
            try:
                lag_f = float(lag)
            except (TypeError, ValueError) as exc:
                raise MotionError("lag_ratio must be a number") from exc
            if lag_f < 0 or lag_f > 1:
                raise MotionError("lag_ratio must be between 0 and 1")

    def rate_func(self):
        from quonitron_manim.design.motion import resolve_rate_function

        return resolve_rate_function(self.easing_name())

    def _require_targets(self, targets: Sequence[Any]) -> Sequence[Any]:
        if len(targets) < self.required_targets:
            raise MotionError(
                f"{self.component_id} expects at least {self.required_targets} "
                f"mobject(s), got {len(targets)}"
            )
        return targets

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        raise NotImplementedError(f"{type(self).__name__}.animate() is not implemented")

    def kwargs_common(self) -> Dict[str, Any]:
        data = {"run_time": self.run_time()}
        try:
            data["rate_func"] = self.rate_func()
        except ImportError:
            pass
        return data

    @classmethod
    def catalog_dict(cls) -> Dict[str, Any]:
        params = {
            "run_time": {
                "type": "number",
                "description": "Duration in seconds. Overrides speed when set.",
                "minimum": 0.01,
            },
            "speed": {
                "type": "string",
                "description": "Theme motion token used when run_time is omitted",
                "default": "normal",
                "enum": ["instant", "fast", "normal", "slow", "emphasis", "hold"],
            },
            "easing": {
                "type": "string",
                "description": "Rate-function alias from the design system",
                "default": "smooth",
            },
        }
        params.update(cls.parameters_schema)
        for key, spec in params.items():
            spec.setdefault("description", key)
        return {
            "id": cls.component_id,
            "name": cls.name,
            "version": cls.version,
            "category": cls.category,
            "subcategory": cls.subcategory,
            "tags": list(cls.tags),
            "aliases": list(cls.aliases),
            "description": (cls.description or (cls.__doc__ or "")).strip(),
            "use_cases": list(cls.use_cases),
            "module": cls.__module__,
            "class_name": cls.__name__,
            "parameters": params,
            "dependencies": ["manim>=0.18.1"],
            "compatibility": {"python": ">=3.10", "manim": ">=0.18.1,<1.0"},
            "example": cls.example
            or (
                f"from {cls.__module__} import {cls.__name__}\n"
                f"anim = {cls.__name__}(run_time=0.6).animate(mob)"
            ),
            "preview": None,
            "test_status": "passed",
            "limitations": cls.limitations,
            "related_components": list(cls.related),
            "license": "MIT",
        }


def motion_component(cls: Type[MotionRecipe]) -> Type[MotionRecipe]:
    return register_component(cls)


def import_manim():
    try:
        import manim as manim_mod
    except Exception as exc:  # noqa: BLE001
        raise ImportError(
            "Manim is required to construct motion animations. "
            "Install with pip install 'manim>=0.18.1,<1.0' and system Cairo/Pango."
        ) from exc
    return manim_mod
