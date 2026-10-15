"""Subtitle-first narration models.

Timings are estimates from reading speed, not alignment to recorded audio.
They remain editable so a human voiceover can be aligned later.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SubtitleCue:
    scene_id: str
    sequence: int
    text: str
    start_seconds: float
    end_seconds: float
    visual_cue: Optional[str] = None

    def __post_init__(self) -> None:
        if self.end_seconds <= self.start_seconds:
            raise ValueError(
                f"Cue {self.sequence} end must be after start "
                f"({self.start_seconds} >= {self.end_seconds})"
            )
        if not self.text.strip():
            raise ValueError("Subtitle text must be non-empty")

    @property
    def duration(self) -> float:
        return self.end_seconds - self.start_seconds

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SubtitleTrack:
    language: str = "en"
    reading_wpm: int = 160
    min_duration: float = 1.2
    max_duration: float = 6.0
    max_line_chars: int = 84
    notes: str = (
        "Estimated timings only. Not synchronized to a recorded speaker."
    )
    cues: List[SubtitleCue] = field(default_factory=list)

    def add(self, cue: SubtitleCue) -> None:
        self.cues.append(cue)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "language": self.language,
            "reading_wpm": self.reading_wpm,
            "min_duration": self.min_duration,
            "max_duration": self.max_duration,
            "max_line_chars": self.max_line_chars,
            "notes": self.notes,
            "cues": [cue.to_dict() for cue in self.cues],
        }
