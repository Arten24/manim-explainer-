"""Split a full narration into readable subtitle cues.

The complete narration stays on the track/timeline so cues can be edited
without losing the source text. Cue IDs are sequential and stay stable when
only timing is overridden later.
"""

from __future__ import annotations

import re
import math
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

    def __post_init__(self):
        if (self.max_chars < 12 or self.reading_wpm <= 0
                or not all(math.isfinite(x) for x in (self.min_duration, self.max_duration, self.sentence_pause, self.comma_pause))
                or self.min_duration <= 0 or self.max_duration < self.min_duration
                or self.sentence_pause < 0 or self.comma_pause < 0
                or any(not str(p).strip() for p in self.protected)):
            raise ValueError("Invalid narration segmentation settings")


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
    settings.__post_init__()
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
    settings.__post_init__()
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


def cues_for_event(narration: str, event, *, id_prefix=None, sequence_start=1,
                   settings=None, lead_in=0.0, lead_out=0.0, gap=0.0):
    """Estimate natural phrases proportionally inside an existing event window.

    Event duration is authoritative. Reading-speed weights are NOT speech alignment.
    Padding applies only to the outer boundaries. Fails rather than compressing gaps.
    IDs derive from the event ID plus stable ordinal, not random state or timestamps.
    """
    from quonitron_manim.timeline.models import LinkedCue
    settings = settings or SegmentSettings()
    settings.__post_init__()
    if not math.isfinite(gap) or gap < 0:
        raise ValueError("gap must be finite and nonnegative")
    texts = split_narration(narration, settings)
    if not texts:
        return []
    available = event.duration - gap * (len(texts) - 1)
    if available <= 0:
        raise ValueError("Gaps consume the event interval")
    weights = [estimate_cue_duration(text, settings) for text in texts]
    cursor, cues = event.start, []
    for index, (text, weight) in enumerate(zip(texts, weights)):
        end = event.end if index == len(texts)-1 else cursor + available * weight / sum(weights)
        cues.append(LinkedCue(id=f"{id_prefix or event.id + '-cue'}-{index+1:03d}",
            scene_id=event.scene_id, sequence=sequence_start+index, text=text,
            start_time=cursor, end_time=end, event_ids=[event.id],
            timing_status="estimated", timing_source="event_window",
            lead_in=lead_in if index == 0 else 0.0,
            lead_out=lead_out if index == len(texts)-1 else 0.0))
        cursor = end + gap
    return cues
