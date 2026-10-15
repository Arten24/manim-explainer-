"""Shared durations and easing names.

Easing names map onto Manim Community ``rate_functions``. Unknown names
fail loudly so scenes cannot silently pick a different motion language.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict

EASING_ALIASES: Dict[str, str] = {
    "smooth": "smooth",
    "linear": "linear",
    "ease_in": "ease_in_cubic",
    "ease_out": "ease_out_cubic",
    "ease_in_out": "ease_in_out_cubic",
    "rush_into": "rush_into",
    "rush_from": "rush_from",
    "there_and_back": "there_and_back",
}


@dataclass(frozen=True)
class Motion:
    instant: float = 0.15
    fast: float = 0.30
    normal: float = 0.60
    slow: float = 1.00
    emphasis: float = 1.20
    hold: float = 0.70
    easing_default: str = "smooth"
    easing_entrance: str = "smooth"
    easing_exit: str = "ease_in"
    easing_emphasis: str = "ease_in_out"

    def duration(self, speed: str = "normal") -> float:
        if not hasattr(self, speed):
            raise ValueError(f"Unknown motion token {speed!r}")
        value = getattr(self, speed)
        if not isinstance(value, (int, float)):
            raise ValueError(f"Motion token {speed!r} is not a duration")
        if float(value) <= 0:
            raise ValueError(f"Motion token {speed!r} must be positive")
        return float(value)


def resolve_rate_function(name: str) -> Callable[[float], float]:
    """Return a Manim rate function. Imports Manim only when called."""
    key = EASING_ALIASES.get(name, name)
    try:
        from manim.utils import rate_functions as rf
    except Exception as exc:  # noqa: BLE001
        raise ImportError(
            f"Cannot load Manim rate functions for easing {name!r}: {exc}"
        ) from exc
    if not hasattr(rf, key):
        raise ValueError(
            f"Unknown easing {name!r} (resolved to {key!r}). "
            f"Known aliases: {sorted(EASING_ALIASES)}"
        )
    return getattr(rf, key)
