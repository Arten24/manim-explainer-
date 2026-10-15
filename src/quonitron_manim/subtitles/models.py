"""Subtitle-first cue and track models.

Timings are estimates from reading speed until a human aligns them to
recorded voiceover. This module never generates audio.
"""

from __future__ import annotations

import math
import re

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


TIMING_STATUSES = frozenset({"estimated", "manual", "manually_aligned", "verified"})


def valid_interval(start, end, label="cue"):
    if not math.isfinite(start) or not math.isfinite(end) or start < 0 or end <= start:
        raise ValueError(f"{label}: end_time must be finite and after nonnegative start_time")


def valid_text(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Cue text must be non-empty")
    if any(ord(c) < 32 and c not in "\n\t" for c in text) or re.search(r"\n[ \t]*\n", text):
        raise ValueError("Cue text cannot contain control characters or blank lines")


def valid_id(value):
    if not isinstance(value, str) or not value.strip() or any(c.isspace() for c in value) or "-->" in value:
        raise ValueError("Cue ID must be nonempty, whitespace-free and not contain -->")


@dataclass
class SubtitleCue:
    id: str
    scene_id: str
    sequence: int
    text: str
    start_time: float
    end_time: float
    visual_cue: Optional[str] = None
    speaker: Optional[str] = None
    event_ids: Optional[list] = None
    timing_status: str = "estimated"
    timing_source: str = "reading_speed"
    alignment_notes: str = ""
    narration_metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Cue id is required")
        if not self.scene_id:
            raise ValueError("scene_id is required")
        if int(self.sequence) < 1:
            raise ValueError("sequence must be >= 1")
        if not str(self.text).strip():
            raise ValueError(f"Cue {self.id}: text must be non-empty")
        valid_id(self.id)
        valid_text(self.text)
        valid_interval(self.start_time, self.end_time, f"Cue {self.id}")
        if self.timing_status not in TIMING_STATUSES:
            raise ValueError(f"{self.id}: invalid timing_status")
        if self.timing_status == "verified" and not (
                self.alignment_notes.strip() and self.narration_metadata.get("audio_reference")):
            raise ValueError(f"{self.id}: verified timing requires review notes and audio_reference")

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SubtitleCue":
        return cls(
            id=str(data["id"]),
            scene_id=str(data["scene_id"]),
            sequence=int(data["sequence"]),
            text=str(data["text"]),
            start_time=float(data["start_time"]),
            end_time=float(data["end_time"]),
            visual_cue=data.get("visual_cue"),
            speaker=data.get("speaker"),
            event_ids=list(data.get("event_ids") or []) or None,
            timing_status=str(data.get("timing_status") or "estimated"),
            timing_source=str(data.get("timing_source") or "reading_speed"),
            alignment_notes=str(data.get("alignment_notes") or ""),
            narration_metadata=dict(data.get("narration_metadata") or {}),
        )


@dataclass
class SubtitleTrack:
    language: str = "en"
    reading_wpm: int = 155
    min_duration: float = 1.2
    max_duration: float = 6.0
    max_chars: int = 84
    overlap_policy: str = "error"
    notes: str = (
        "Estimated timings only. Not synchronized to a recorded speaker. "
        "Edit these cues when aligning a real voiceover."
    )
    cues: List[SubtitleCue] = field(default_factory=list)
    preserve_lines: bool = False

    def add(self, cue: SubtitleCue) -> None:
        self.cues.append(cue)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "language": self.language,
            "reading_wpm": self.reading_wpm,
            "min_duration": self.min_duration,
            "max_duration": self.max_duration,
            "max_chars": self.max_chars,
            "overlap_policy": self.overlap_policy,
            "notes": self.notes,
            "cues": [cue.to_dict() for cue in self.cues],
            "preserve_lines": self.preserve_lines,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SubtitleTrack":
        track = cls(
            language=data.get("language", "en"),
            reading_wpm=int(data.get("reading_wpm", 155)),
            min_duration=float(data.get("min_duration", 1.2)),
            max_duration=float(data.get("max_duration", 6.0)),
            max_chars=int(data.get("max_chars", 84)),
            overlap_policy=str(data.get("overlap_policy", "error")),
            notes=str(data.get("notes", cls.notes)),
            preserve_lines=bool(data.get("preserve_lines", False)),
        )
        for raw in data.get("cues") or []:
            track.add(SubtitleCue.from_dict(raw))
        return track


@dataclass(frozen=True)
class SubtitleStyle:
    """Insets within the shared subtitle reservation; never expands into content."""
    max_lines: int = 2
    max_width: Optional[float] = None
    padding: float = 0.04
    safe_margin: Optional[float] = None
    line_gap: float = 0.08
    speaker_labels: bool = False

    def __post_init__(self):
        if not isinstance(self.max_lines, int) or self.max_lines < 1:
            raise ValueError("max_lines must be a positive integer")
        for value in (self.padding, self.line_gap, self.safe_margin):
            if value is not None and (not math.isfinite(value) or value < 0):
                raise ValueError("Subtitle insets must be finite and nonnegative")
        if self.max_width is not None and (not math.isfinite(self.max_width) or self.max_width <= 0):
            raise ValueError("max_width must be finite and positive")

    def region(self, theme):
        from quonitron_manim.design.layout import SafeArea, LayoutError, layout_regions
        band = layout_regions(theme.frame_width, theme.frame_height, theme.spacing.safe_margin)["subtitle"]
        extra = max(0, (self.safe_margin or 0) - theme.spacing.safe_margin)
        left, right = band.left + self.padding + extra, band.right - self.padding - extra
        if self.max_width is not None and self.max_width < right - left:
            middle = (left + right) / 2
            left, right = middle - self.max_width / 2, middle + self.max_width / 2
        area = SafeArea(left, right, band.bottom + self.padding + extra, band.top - self.padding)
        if area.width <= 0 or area.height <= 0:
            raise LayoutError("Subtitle padding/margins leave no usable space")
        return area
