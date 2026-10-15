"""Detect a usable Manim + Cairo stack without crashing unit tests."""

from __future__ import annotations

from typing import Optional, Tuple


def cairo_usable() -> Tuple[bool, str]:
    try:
        import cairo  # type: ignore
    except Exception as exc:  # noqa: BLE001
        return False, f"pycairo import failed: {exc}"
    version = getattr(cairo, "__version__", "")
    if "stub" in str(version).lower():
        return False, "pycairo is a local stub, not a real Cairo binding"
    try:
        fmt = getattr(cairo, "FORMAT_ARGB32", None)
        if fmt is None:
            fmt = cairo.Format.ARGB32  # type: ignore[attr-defined]
        surface = cairo.ImageSurface(fmt, 8, 8)
        width = surface.get_width()
        if width != 8:
            return False, "Cairo ImageSurface did not report expected width"
    except Exception as exc:  # noqa: BLE001
        return False, f"Cairo surface test failed: {exc}"
    return True, f"cairo {version or 'ok'}"


def manimpango_usable() -> Tuple[bool, str]:
    try:
        import manimpango  # type: ignore
    except Exception as exc:  # noqa: BLE001
        return False, f"manimpango import failed: {exc}"
    if getattr(manimpango, "MarkupUtils", None) is object or not hasattr(
        manimpango, "list_fonts"
    ):
        return False, "manimpango API missing"
    try:
        fonts = manimpango.list_fonts()
    except Exception as exc:  # noqa: BLE001
        return False, f"manimpango.list_fonts failed: {exc}"
    if not fonts:
        # An empty list can still mean a real binding with no fonts, but
        # our stub also returns []. Treat empty as unusable for Text.
        return False, "manimpango.list_fonts() returned no fonts"
    return True, f"{len(fonts)} fonts"


def manim_available() -> bool:
    try:
        import manim  # noqa: F401
    except Exception:
        return False
    ok, _ = cairo_usable()
    return ok


def import_error_message() -> Optional[str]:
    cairo_ok, cairo_msg = cairo_usable()
    pango_ok, pango_msg = manimpango_usable()
    if cairo_ok and pango_ok:
        return None
    parts = []
    if not cairo_ok:
        parts.append(cairo_msg)
    if not pango_ok:
        parts.append(pango_msg)
    return "; ".join(parts)
