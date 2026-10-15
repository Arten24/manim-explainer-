"""Render configuration defaults. Full render pipelines arrive in later parts."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict

from quonitron.design import get_theme


@dataclass
class RenderConfig:
    quality: str = "ql"  # manim -ql preview; later: qm, qh, qk
    preview: bool = True
    write_to_movie: bool = True
    save_last_frame: bool = True
    disable_caching: bool = True
    pixel_width: int = 854
    pixel_height: int = 480
    frame_rate: int = 15
    background_color: str = "#0B0F19"

    @classmethod
    def preview_defaults(cls) -> "RenderConfig":
        theme = get_theme()
        return cls(background_color=theme.color("background"))

    @classmethod
    def production_defaults(cls) -> "RenderConfig":
        theme = get_theme()
        return cls(
            quality="qh",
            preview=False,
            pixel_width=theme.pixel_width,
            pixel_height=theme.pixel_height,
            frame_rate=theme.frame_rate,
            background_color=theme.color("background"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
