"""QUONITRON Manim Master Library.

An extensible, reusable animation component library for educational video
production with Manim Community Edition.
"""

__version__ = "0.1.0"
__catalog_version__ = "1.0.0"

from quonitron.design import Theme, get_theme, register_theme

__all__ = [
    "__version__",
    "__catalog_version__",
    "Theme",
    "get_theme",
    "register_theme",
]
