"""Split a full narration into readable subtitle cues.

The complete narration stays on the track/timeline so cues can be edited
without losing the source text. Cue IDs are sequential and stay stable when
only timing is overridden later.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List, Sequence

from quonitron_manim.subtitles.export import estimate_duration

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
SOFT_SPLIT = re.compile(r"(?<=[,;:])\s+")

DEFAULT_PROTECTED = (
    "variable name",
    "programming language",
    "memory address",
    "equals ten",
)


@dataclass
class SegmentSettings:
    max_chars: int = 84
    min_duration: float = 1.35
    max_duration: float = 6.5
    reading_wpm: int = 150
    sentence_pause: float = 0.28
    comma_pause: float = 0.08
    protected: Sequence[str] = DEFAULT_PROTECTED


def _protect_ok(text: str, cut: int, protected: Sequence[str]) -> bool:
    lower = text.lower()
    for phrase in protected:
        start = 0
        needle = phrase.lower()
        while True:
            idx = lower.find(needle, start)
            if idx < 0:
                break
            end = idx + len(needle)
            if idx < cut < end:
                return False
            start = idx + 1
    return True


def _split_long(text: str, max_chars: int, protected: Sequence[str]) -> List[str]:
    text = " ".join(text.split())
    if len(text) <= max_chars:
        return [text]
    parts: List[str] = []
    remaining = text
    while remaining:
        if len(remaining) <= max_chars:
            parts.append(remaining)
            break
        window = remaining[: max_chars + 1]
        cut = -1
        for match in SOFT_SPLIT.finditer(window):
            if match.end() <= max_chars and _protect_ok(remaining, match.end(), protected):
                cut = match.end()
        if cut < 12:
            cut = window.rfind(" ")
            while cut > 12 and not _protect_ok(remaining, cut, protected):
                cut = remaining.rfind(" ", 0, cut)
        if cut < 12:
            cut = max_chars
        piece = remaining[:cut].strip()
        remaining = remaining[cut:].strip()
        if piece:
            parts.append(piece)
    return parts


def split_narration(narration: str, settings: SegmentSettings | None = None) -> List[str]:
    settings = settings or SegmentSettings()
    compact = " ".join(narration.strip().split())
    if not compact:
        return []
    sentences = [s.strip() for s in SENTENCE_SPLIT.split(compact) if s.strip()]
    cues: List[str] = []
    for sentence in sentences:
        cues.extend(_split_long(sentence, settings.max_chars, settings.protected))
    return cues


def estimate_cue_duration(text: str, settings: SegmentSettings) -> float:
    base = estimate_duration(
        text, settings.reading_wpm, settings.min_duration, settings.max_duration
    )
    extra = 0.0
    stripped = text.rstrip()
    if stripped.endswith((".", "?", "!")):
        extra += settings.sentence_pause
    elif stripped.endswith((",", ";", ":")):
        extra += settings.comma_pause
    if stripped.endswith(("…", "...")):
        extra += settings.sentence_pause
    value = min(settings.max_duration, base + extra)
    return max(settings.min_duration, value)


def pack_cues(
    texts: Iterable[str],
    *,
    scene_id: str,
    id_prefix: str = "cue",
    start_at: float = 0.0,
    settings: SegmentSettings | None = None,
    event_ids_for: Sequence[Sequence[str]] | None = None,
):
    from quonitron_manim.timeline.models import LinkedCue

    settings = settings or SegmentSettings()
    cursor = start_at
    cues = []
    for index, text in enumerate(texts, start=1):
        dur = estimate_cue_duration(text, settings)
        links: List[str] = []
        if event_ids_for is not None and index - 1 < len(event_ids_for):
            links = list(event_ids_for[index - 1])
        cues.append(
            LinkedCue(
                id=f"{id_prefix}-{index:03d}",
                scene_id=scene_id,
                sequence=index,
                text=text,
                start_time=round(cursor, 3),
                end_time=round(cursor + dur, 3),
                event_ids=links,
                timing_status="estimated",
            )
        )
        cursor += dur
    return cues
