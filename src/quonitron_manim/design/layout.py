"""Margins, safe areas, spacing scale, and stroke tokens.

Manim's default frame is 8 units tall. At 16:9 the width is 14.222….
Values here are in those scene units, not pixels.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Spacing:
    """Spacing scale. Use these instead of magic numbers in scenes."""

    xxs: float = 0.08
    xs: float = 0.16
    sm: float = 0.28
    md: float = 0.40
    lg: float = 0.64
    xl: float = 1.00
    margin: float = 0.55
    safe_margin: float = 0.80
    gutter: float = 0.40
    card_padding: float = 0.32
    title_to_content: float = 0.70


@dataclass(frozen=True)
class Stroke:
    hairline: float = 1.0
    thin: float = 1.5
    regular: float = 2.25
    thick: float = 3.5
    corner_radius: float = 0.16


@dataclass(frozen=True)
class SafeArea:
    left: float
    right: float
    bottom: float
    top: float

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.top - self.bottom


def safe_area(
    frame_width: float = 14.222222,
    frame_height: float = 8.0,
    margin: float = 0.80,
) -> SafeArea:
    half_w = frame_width / 2.0
    half_h = frame_height / 2.0
    return SafeArea(
        left=-half_w + margin,
        right=half_w - margin,
        bottom=-half_h + margin,
        top=half_h - margin,
    )


def title_anchor(area: SafeArea, lift: float = 0.15) -> Tuple[float, float, float]:
    """World coordinates for a top-centered title."""
    return (0.0, area.top - lift, 0.0)


def subtitle_anchor(area: SafeArea, drop: float = 0.10) -> Tuple[float, float, float]:
    """World coordinates for a bottom caption / subtitle cue."""
    return (0.0, area.bottom + drop, 0.0)
