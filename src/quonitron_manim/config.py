"""Library-wide configuration and render profiles.

Manim CLI flags still win at render time. These profiles are the defaults
the base scene and demo scripts apply when a theme is loaded.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class RenderProfile:
    """Pixel size, frame rate, and quality shorthand for Manim."""

    name: str
    quality_flag: str
    pixel_width: int
    pixel_height: int
    frame_rate: int
    preview: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


PREVIEW = RenderProfile(
    name="preview",
    quality_flag="ql",
    pixel_width=854,
    pixel_height=480,
    frame_rate=15,
    preview=True,
)

STANDARD = RenderProfile(
    name="standard",
    quality_flag="qm",
    pixel_width=1280,
    pixel_height=720,
    frame_rate=30,
    preview=False,
)

PRODUCTION = RenderProfile(
    name="production",
    quality_flag="qh",
    pixel_width=1920,
    pixel_height=1080,
    frame_rate=30,
    preview=False,
)

PROFILES = {
    "preview": PREVIEW,
    "ql": PREVIEW,
    "low": PREVIEW,
    "standard": STANDARD,
    "qm": STANDARD,
    "medium": STANDARD,
    "production": PRODUCTION,
    "qh": PRODUCTION,
    "high": PRODUCTION,
}

DEFAULT_PROFILE_NAME = "standard"


def get_render_profile(name: Optional[str] = None) -> RenderProfile:
    key = (name or DEFAULT_PROFILE_NAME).lower()
    if key not in PROFILES:
        raise ValueError(
            f"Unknown render profile {name!r}. "
            f"Available: {sorted(set(p.name for p in PROFILES.values()))}"
        )
    return PROFILES[key]


def apply_profile_to_manim(profile: RenderProfile) -> None:
    """Push a profile into ``manim.config`` when Manim is importable."""
    from quonitron_manim.core.manim_compat import manim_available

    if not manim_available():
        return
    from manim import config

    config.pixel_width = profile.pixel_width
    config.pixel_height = profile.pixel_height
    config.frame_rate = profile.frame_rate


def override_profile(profile: RenderProfile, **changes: Any) -> RenderProfile:
    return replace(profile, **changes)
