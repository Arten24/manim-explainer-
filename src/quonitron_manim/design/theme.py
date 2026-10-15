"""Semantic color roles and the swappable QUONITRON theme."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from typing import Any, Dict, Mapping, Optional

from quonitron_manim.design.layout import Spacing, Stroke
from quonitron_manim.design.motion import Motion
from quonitron_manim.design.typography import Typography


@dataclass(frozen=True)
class ColorPalette:
    """Semantic colors. Pass roles, not raw hex, into components."""

    background: str = "#0D1117"
    surface: str = "#161B22"
    surface_elevated: str = "#1C2333"
    text_primary: str = "#F5F7FA"
    text_secondary: str = "#9AA4B2"
    text_muted: str = "#6E7A8A"
    accent: str = "#4C8DFF"
    accent_secondary: str = "#8B7CFF"
    highlight: str = "#5EC8C5"
    success: str = "#3DDC97"
    warning: str = "#E3B341"
    danger: str = "#F85149"
    grid: str = "#21262D"
    border: str = "#30363D"
    equation: str = "#E8ECF4"
    code_bg: str = "#0B1018"


def _is_hex_color(value: str) -> bool:
    if not isinstance(value, str) or not value.startswith("#"):
        return False
    body = value[1:]
    return len(body) in (3, 6, 8) and all(c in "0123456789abcdefABCDEF" for c in body)


@dataclass(frozen=True)
class Theme:
    """Complete visual identity. Components accept a Theme, never ad-hoc styles."""

    name: str = "quonitron_dark"
    colors: ColorPalette = field(default_factory=ColorPalette)
    typography: Typography = field(default_factory=Typography)
    spacing: Spacing = field(default_factory=Spacing)
    stroke: Stroke = field(default_factory=Stroke)
    motion: Motion = field(default_factory=Motion)
    background_opacity: float = 1.0
    frame_width: float = 14.222222
    frame_height: float = 8.0
    render_profile: str = "standard"

    def color(self, role: str) -> str:
        if not hasattr(self.colors, role):
            raise ValueError(
                f"Unknown color role {role!r}. "
                f"Available: {sorted(self.colors.__dataclass_fields__)}"
            )
        value = getattr(self.colors, role)
        if not _is_hex_color(value):
            raise ValueError(f"Color role {role!r} is not a hex color: {value!r}")
        return value

    def duration(self, speed: str = "normal") -> float:
        return self.motion.duration(speed)

    def override(
        self,
        *,
        name: Optional[str] = None,
        colors: Optional[Mapping[str, str]] = None,
        **kwargs: Any,
    ) -> "Theme":
        """Return a copy with selected fields or color roles replaced."""
        new_colors = self.colors
        if colors:
            unknown = set(colors) - set(self.colors.__dataclass_fields__)
            if unknown:
                raise ValueError(f"Unknown color roles in override: {sorted(unknown)}")
            new_colors = replace(self.colors, **dict(colors))
        return replace(self, name=name or self.name, colors=new_colors, **kwargs)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


THEMES: Dict[str, Theme] = {}
DEFAULT_THEME_NAME = "quonitron_dark"


def register_theme(name: str, theme: Theme) -> Theme:
    if not name or not name.strip():
        raise ValueError("Theme name must be non-empty")
    THEMES[name] = theme
    return theme


def get_theme(name: Optional[str] = None) -> Theme:
    key = name or DEFAULT_THEME_NAME
    if key not in THEMES:
        raise ValueError(f"Unknown theme {key!r}. Registered: {sorted(THEMES)}")
    return THEMES[key]


def list_themes() -> list[str]:
    return sorted(THEMES)


def apply_theme_to_manim(theme: Optional[Theme] = None) -> None:
    """Set Manim ``config.background_color`` from the theme when possible."""
    theme = theme or get_theme()
    from quonitron_manim.core.manim_compat import manim_available

    if not manim_available():
        return
    from manim import config

    config.background_color = theme.color("background")
    config.background_opacity = theme.background_opacity


register_theme(DEFAULT_THEME_NAME, Theme())
