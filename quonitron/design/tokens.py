"""Design tokens for the QUONITRON visual identity.

These values are the single source of truth for color, type, spacing, and
motion. Animation components must read from a Theme rather than hard-coding
visual constants. Themes are swappable without changing component APIs.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ColorPalette:
    """Semantic color roles. Values are hex strings (#RRGGBB)."""

    background: str = "#0B0F19"
    surface: str = "#141A2A"
    surface_elevated: str = "#1C2336"
    text_primary: str = "#F5F7FA"
    text_secondary: str = "#A9B4C7"
    text_muted: str = "#6B768A"
    accent: str = "#4F8CFF"
    accent_secondary: str = "#7C5CFF"
    success: str = "#3DDC97"
    warning: str = "#FFB020"
    danger: str = "#FF5A5F"
    grid: str = "#1F2738"
    border: str = "#2A3348"
    highlight: str = "#5EEAD4"
    equation: str = "#E8ECF4"


@dataclass(frozen=True)
class Typography:
    """Type hierarchy and font fallbacks.

    Manim will try fonts in order. Bundled/system fallbacks keep renders
    portable across Windows, macOS, and Linux.
    """

    font_primary: str = "DejaVu Sans"
    font_primary_fallbacks: tuple = (
        "Inter",
        "Liberation Sans",
        "Arial",
        "Helvetica",
        "sans-serif",
    )
    font_monospace: str = "DejaVu Sans Mono"
    font_monospace_fallbacks: tuple = (
        "Liberation Mono",
        "Consolas",
        "Courier New",
        "monospace",
    )
    font_math: str = "TeX Gyre Termes"
    title_size: float = 48.0
    heading_size: float = 36.0
    body_size: float = 28.0
    label_size: float = 22.0
    caption_size: float = 18.0
    line_spacing: float = 1.2
    title_weight: str = "BOLD"
    heading_weight: str = "MEDIUM"
    body_weight: str = "NORMAL"


@dataclass(frozen=True)
class Spacing:
    """Scene margins and layout gaps, in Manim scene units."""

    margin: float = 0.6
    safe_margin: float = 0.8
    gutter: float = 0.4
    card_padding: float = 0.35
    element_gap: float = 0.25
    title_lift: float = 3.2


@dataclass(frozen=True)
class Motion:
    """Shared duration and easing conventions, in seconds."""

    instant: float = 0.12
    fast: float = 0.25
    normal: float = 0.5
    slow: float = 0.9
    emphasis: float = 1.2
    hold: float = 0.8
    easing_default: str = "smooth"
    easing_entrance: str = "smooth"
    easing_exit: str = "smooth"


@dataclass(frozen=True)
class Stroke:
    hairline: float = 1.0
    thin: float = 1.5
    regular: float = 2.0
    thick: float = 3.5
    corner_radius: float = 0.18


@dataclass
class Theme:
    """Complete visual identity. Components accept a Theme instance."""

    name: str = "quonitron_dark"
    colors: ColorPalette = field(default_factory=ColorPalette)
    typography: Typography = field(default_factory=Typography)
    spacing: Spacing = field(default_factory=Spacing)
    motion: Motion = field(default_factory=Motion)
    stroke: Stroke = field(default_factory=Stroke)
    background_opacity: float = 1.0
    shadow_opacity: float = 0.25
    frame_width: float = 14.222  # 16:9 at default Manim height 8
    frame_height: float = 8.0
    pixel_width: int = 1920
    pixel_height: int = 1080
    frame_rate: int = 30

    def color(self, role: str) -> str:
        if not hasattr(self.colors, role):
            raise ValueError(f"Unknown color role: {role}")
        return getattr(self.colors, role)

    def duration(self, speed: str = "normal") -> float:
        if not hasattr(self.motion, speed):
            raise ValueError(f"Unknown motion token: {speed}")
        value = getattr(self.motion, speed)
        if not isinstance(value, (int, float)):
            raise ValueError(f"Motion token {speed!r} is not a duration")
        return float(value)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


THEMES: Dict[str, Theme] = {}

DEFAULT_THEME_NAME = "quonitron_dark"


def register_theme(name: str, theme: Theme) -> Theme:
    if not name:
        raise ValueError("Theme name must be non-empty")
    THEMES[name] = theme
    return theme


def get_theme(name: Optional[str] = None) -> Theme:
    key = name or DEFAULT_THEME_NAME
    if key not in THEMES:
        raise ValueError(
            f"Unknown theme: {key}. Registered: {sorted(THEMES)}"
        )
    return THEMES[key]


def list_themes() -> List[str]:
    return sorted(THEMES)


register_theme(DEFAULT_THEME_NAME, Theme())
