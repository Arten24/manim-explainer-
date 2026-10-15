"""Subtitle-first cue and track models.

Timings are estimates from reading speed until a human aligns them to
recorded voiceover. This module never generates audio.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


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

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Cue id is required")
        if not self.scene_id:
            raise ValueError("scene_id is required")
        if int(self.sequence) < 1:
            raise ValueError("sequence must be >= 1")
        if not str(self.text).strip():
            raise ValueError(f"Cue {self.id}: text must be non-empty")
        if self.start_time < 0 or self.end_time < 0:
            raise ValueError(f"Cue {self.id}: times must be >= 0")
        if self.end_time <= self.start_time:
            raise ValueError(
                f"Cue {self.id}: end_time ({self.end_time}) must be after "
                f"start_time ({self.start_time})"
            )

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
        )
        for raw in data.get("cues") or []:
            track.add(SubtitleCue.from_dict(raw))
        return track
