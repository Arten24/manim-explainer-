"""Type hierarchy and portable font fallbacks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Sequence, Tuple


# Manim Text.font_list() needs manimpango. These names are tried in order.
DEFAULT_SANS: Tuple[str, ...] = (
    "DejaVu Sans",
    "Liberation Sans",
    "Noto Sans",
    "Inter",
    "Segoe UI",
    "Arial",
    "Helvetica",
    "sans-serif",
)

DEFAULT_MONO: Tuple[str, ...] = (
    "DejaVu Sans Mono",
    "Liberation Mono",
    "Cascadia Mono",
    "Consolas",
    "Courier New",
    "monospace",
)


@dataclass(frozen=True)
class TextStyle:
    """One step in the type hierarchy, in Manim ``font_size`` units."""

    role: str
    font_size: float
    color_role: str
    weight: str = "NORMAL"
    slant: str = "NORMAL"
    family: str = "sans"


@dataclass(frozen=True)
class Typography:
    font_sans: Tuple[str, ...] = DEFAULT_SANS
    font_mono: Tuple[str, ...] = DEFAULT_MONO
    line_spacing: float = 1.15
    title: TextStyle = field(
        default_factory=lambda: TextStyle("title", 48.0, "text_primary", "BOLD")
    )
    heading: TextStyle = field(
        default_factory=lambda: TextStyle("heading", 36.0, "text_primary", "MEDIUM")
    )
    body: TextStyle = field(
        default_factory=lambda: TextStyle("body", 28.0, "text_primary")
    )
    label: TextStyle = field(
        default_factory=lambda: TextStyle("label", 22.0, "text_secondary")
    )
    caption: TextStyle = field(
        default_factory=lambda: TextStyle("caption", 20.0, "text_secondary")
    )
    code: TextStyle = field(
        default_factory=lambda: TextStyle(
            "code", 26.0, "highlight", family="mono"
        )
    )

    def style(self, role: str) -> TextStyle:
        if not hasattr(self, role) or role in {"font_sans", "font_mono", "line_spacing"}:
            raise ValueError(f"Unknown text role {role!r}")
        value = getattr(self, role)
        if not isinstance(value, TextStyle):
            raise ValueError(f"{role!r} is not a TextStyle")
        return value

    def family_stack(self, family: str = "sans") -> Tuple[str, ...]:
        if family == "mono":
            return self.font_mono
        if family == "sans":
            return self.font_sans
        raise ValueError(f"Unknown font family {family!r}")


def list_system_fonts() -> List[str]:
    try:
        import manimpango  # type: ignore

        fonts = list(manimpango.list_fonts())
        return fonts
    except Exception:
        return []


def resolve_font(stack: Sequence[str], available: Iterable[str] | None = None) -> str:
    """Return the first font that exists, else the first requested name.

    Manim warns on missing fonts and still renders with a default. We never
    assume Inter or any premium face is installed.
    """
    names = list(stack)
    if not names:
        return "sans-serif"
    catalog = list(available) if available is not None else list_system_fonts()
    if not catalog:
        return names[0]
    lowered = {item.lower(): item for item in catalog}
    for name in names:
        if name in catalog:
            return name
        match = lowered.get(name.lower())
        if match:
            return match
    return names[0]
