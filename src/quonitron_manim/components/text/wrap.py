"""Plain-text wrapping and highlight splitting. No Manim import."""

from __future__ import annotations

import re
from typing import List, Sequence, Tuple

_WORD = re.compile(r"\s+")


class TextLayoutError(ValueError):
    """Invalid text component parameters."""


def wrap_plain_text(text: str, max_chars: int) -> List[str]:
    """Word-wrap ``text`` to ``max_chars`` without breaking the last word when possible."""
    blob = " ".join(str(text).split())
    if not blob:
        return []
    if max_chars < 8:
        raise TextLayoutError("max_chars must be >= 8")
    if len(blob) <= max_chars:
        return [blob]
    lines: List[str] = []
    remaining = blob
    while remaining:
        if len(remaining) <= max_chars:
            lines.append(remaining)
            break
        window = remaining[: max_chars + 1]
        cut = window.rfind(" ")
        if cut < 4:
            cut = max_chars
        piece = remaining[:cut].strip()
        remaining = remaining[cut:].strip()
        if piece:
            lines.append(piece)
    return lines


def chars_for_width(max_width: float, font_size: float) -> int:
    """Heuristic character budget from scene width and Manim font_size.

    Tuned for QUONITRON body type (~28) on a ~12.6-unit content band.
    """
    if max_width <= 0 or font_size <= 0:
        raise TextLayoutError("max_width and font_size must be positive")
    em = float(font_size) * 0.0115
    return max(8, int(float(max_width) / em))


def highlight_parts(text: str, phrase: str) -> Tuple[str, str, str]:
    """Split ``text`` into (before, phrase, after). Phrase match is case-sensitive."""
    source = str(text)
    needle = str(phrase)
    if not needle:
        raise TextLayoutError("highlight phrase must be non-empty")
    idx = source.find(needle)
    if idx < 0:
        raise TextLayoutError(f"phrase {needle!r} is not in {source!r}")
    return source[:idx], needle, source[idx + len(needle) :]


def normalize_items(items: Sequence[str]) -> List[str]:
    cleaned = [str(item).strip() for item in items]
    if not cleaned or any(not item for item in cleaned):
        raise TextLayoutError("list items must be a non-empty sequence of strings")
    return cleaned
