"""QUONITRON Manim Master Library — Parts 1–3."""

from __future__ import annotations

__version__ = "0.4.0"
__catalog_schema_version__ = "1.0.0"

from quonitron_manim.config import RenderProfile, get_render_profile
from quonitron_manim.design.theme import Theme, get_theme, register_theme

__all__ = [
    "__version__",
    "__catalog_schema_version__",
    "Theme",
    "get_theme",
    "register_theme",
    "RenderProfile",
    "get_render_profile",
]
