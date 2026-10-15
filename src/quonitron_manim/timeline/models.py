"""Shared subtitle + animation timeline.

Seconds are canonical. Frame numbers are derived from the configured
frame rate and are never stored as a second clock.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

TIMING_STATUSES = frozenset({"estimated", "manual"})


def _positive_interval(start: float, end: float, label: str) -> None:
    if start < 0 or end < 0:
        raise ValueError(f"{label}: times must be >= 0")
    if end <= start:
        raise ValueError(f"{label}: end ({end}) must be after start ({start})")


@dataclass
class SceneWindow:
    scene_id: str
    start: float
    end: float
    title: str = ""

    def __post_init__(self) -> None:
        if not self.scene_id:
            raise ValueError("scene_id is required")
        _positive_interval(self.start, self.end, f"scene {self.scene_id}")

    @property
    def duration(self) -> float:
        return self.end - self.start

    def contains(self, start: float, end: float, *, tol: float = 1e-6) -> bool:
        return start >= self.start - tol and end <= self.end + tol

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SceneWindow":
        return cls(
            scene_id=str(data["scene_id"]),
            start=float(data["start"]),
            end=float(data["end"]),
            title=str(data.get("title") or ""),
        )


@dataclass
class VisualEvent:
    id: str
    scene_id: str
    motion_id: str
    start: float
    end: float
    label: str = ""
    depends_on: List[str] = field(default_factory=list)
    overlap_ok: bool = False
    pause_after: float = 0.0
    play_duration: Optional[float] = None
    params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("VisualEvent.id is required")
        if not self.scene_id:
            raise ValueError(f"{self.id}: scene_id is required")
        if not self.motion_id:
            raise ValueError(f"{self.id}: motion_id is required")
        _positive_interval(self.start, self.end, f"event {self.id}")
        if self.pause_after < 0:
            raise ValueError(f"{self.id}: pause_after must be >= 0")
        if self.play_duration is not None and self.play_duration <= 0:
            raise ValueError(f"{self.id}: play_duration must be positive")
        if self.play_duration is not None and self.play_duration - 1e-6 > self.duration:
            raise ValueError(
                f"{self.id}: play_duration {self.play_duration} exceeds interval "
                f"{self.duration}"
            )

    @property
    def duration(self) -> float:
        return self.end - self.start

    def animation_duration(self) -> float:
        """Time actually passed to Scene.play. May be shorter than the semantic interval."""
        if self.play_duration is not None:
            return float(self.play_duration)
        return self.duration

    def play_end(self) -> float:
        return self.start + self.animation_duration()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VisualEvent":
        return cls(
            id=str(data["id"]),
            scene_id=str(data["scene_id"]),
            motion_id=str(data["motion_id"]),
            start=float(data["start"]),
            end=float(data["end"]),
            label=str(data.get("label") or ""),
            depends_on=list(data.get("depends_on") or []),
            overlap_ok=bool(data.get("overlap_ok", False)),
            pause_after=float(data.get("pause_after") or 0.0),
            play_duration=(
                float(data["play_duration"])
                if data.get("play_duration") is not None
                else None
            ),
            params=dict(data.get("params") or {}),
        )


@dataclass
class LinkedCue:
    """Subtitle cue bound to the same clock as visual events."""

    id: str
    scene_id: str
    sequence: int
    text: str
    start_time: float
    end_time: float
    event_ids: List[str] = field(default_factory=list)
    visual_cue: Optional[str] = None
    speaker: Optional[str] = None
    timing_status: str = "estimated"
    manual_start: Optional[float] = None
    manual_end: Optional[float] = None

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("cue id is required")
        if not self.scene_id:
            raise ValueError(f"{self.id}: scene_id is required")
        if int(self.sequence) < 1:
            raise ValueError(f"{self.id}: sequence must be >= 1")
        if not str(self.text).strip():
            raise ValueError(f"{self.id}: text must be non-empty")
        if self.timing_status not in TIMING_STATUSES:
            raise ValueError(
                f"{self.id}: timing_status must be one of {sorted(TIMING_STATUSES)}"
            )
        _positive_interval(self.start_time, self.end_time, f"cue {self.id} estimate")
        if self.manual_start is not None or self.manual_end is not None:
            if self.manual_start is None or self.manual_end is None:
                raise ValueError(f"{self.id}: manual start and end must both be set")
            _positive_interval(self.manual_start, self.manual_end, f"cue {self.id} manual")

    def effective_start(self) -> float:
        if self.timing_status == "manual" and self.manual_start is not None:
            return float(self.manual_start)
        return self.start_time

    def effective_end(self) -> float:
        if self.timing_status == "manual" and self.manual_end is not None:
            return float(self.manual_end)
        return self.end_time

    @property
    def duration(self) -> float:
        return self.effective_end() - self.effective_start()

    def override_timing(self, start: float, end: float) -> None:
        _positive_interval(start, end, f"cue {self.id} override")
        self.manual_start = start
        self.manual_end = end
        self.timing_status = "manual"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LinkedCue":
        return cls(
            id=str(data["id"]),
            scene_id=str(data["scene_id"]),
            sequence=int(data["sequence"]),
            text=str(data["text"]),
            start_time=float(data["start_time"]),
            end_time=float(data["end_time"]),
            event_ids=list(data.get("event_ids") or []),
            visual_cue=data.get("visual_cue"),
            speaker=data.get("speaker"),
            timing_status=str(data.get("timing_status") or "estimated"),
            manual_start=(
                float(data["manual_start"])
                if data.get("manual_start") is not None
                else None
            ),
            manual_end=(
                float(data["manual_end"]) if data.get("manual_end") is not None else None
            ),
        )


@dataclass
class Timeline:
    scene: SceneWindow
    events: List[VisualEvent] = field(default_factory=list)
    cues: List[LinkedCue] = field(default_factory=list)
    narration: str = ""
    frame_rate: float = 30.0
    reading_wpm: int = 155
    notes: str = (
        "Estimated timings share this clock with visual events. They are not "
        "aligned to a recorded speaker until timing_status is set to manual."
    )

    def __post_init__(self) -> None:
        if self.frame_rate <= 0:
            raise ValueError("frame_rate must be positive")

    def seconds_to_frames(self, seconds: float) -> int:
        return int(round(float(seconds) * float(self.frame_rate)))

    def frames_to_seconds(self, frames: int) -> float:
        return float(frames) / float(self.frame_rate)

    def event_by_id(self, event_id: str) -> VisualEvent:
        for event in self.events:
            if event.id == event_id:
                return event
        known = ", ".join(e.id for e in self.events) or "(none)"
        raise KeyError(f"Unknown event id {event_id!r}. Known: {known}")

    def cue_by_id(self, cue_id: str) -> LinkedCue:
        for cue in self.cues:
            if cue.id == cue_id:
                return cue
        known = ", ".join(c.id for c in self.cues) or "(none)"
        raise KeyError(f"Unknown cue id {cue_id!r}. Known: {known}")

    def cue_at(self, time: float) -> Optional[LinkedCue]:
        for cue in self.cues:
            if cue.effective_start() - 1e-9 <= time < cue.effective_end() - 1e-12:
                return cue
        return None

    def events_at(self, time: float) -> List[VisualEvent]:
        return [
            event
            for event in self.events
            if event.start - 1e-9 <= time < event.end - 1e-12
        ]

    def rescale_event(
        self,
        event_id: str,
        new_duration: float,
        *,
        shift_following: bool = True,
    ) -> None:
        event = self.event_by_id(event_id)
        if new_duration <= 0:
            raise ValueError("new_duration must be positive")
        old_end = event.end
        delta = new_duration - event.duration
        event.end = event.start + new_duration
        if shift_following and abs(delta) > 1e-9:
            for other in self.events:
                if other.id == event.id:
                    continue
                if other.start >= old_end - 1e-9:
                    other.start += delta
                    other.end += delta
            for cue in self.cues:
                if cue.timing_status == "manual":
                    continue
                if cue.start_time >= old_end - 1e-9:
                    cue.start_time += delta
                    cue.end_time += delta
        self.scene.end = max(
            self.scene.end,
            max((e.end for e in self.events), default=self.scene.end),
            max((c.effective_end() for c in self.cues), default=self.scene.end),
        )

    def override_cue(self, cue_id: str, start: float, end: float) -> None:
        self.cue_by_id(cue_id).override_timing(start, end)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scene": self.scene.to_dict(),
            "events": [event.to_dict() for event in self.events],
            "cues": [cue.to_dict() for cue in self.cues],
            "narration": self.narration,
            "frame_rate": self.frame_rate,
            "reading_wpm": self.reading_wpm,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Timeline":
        return cls(
            scene=SceneWindow.from_dict(data["scene"]),
            events=[VisualEvent.from_dict(item) for item in data.get("events") or []],
            cues=[LinkedCue.from_dict(item) for item in data.get("cues") or []],
            narration=str(data.get("narration") or ""),
            frame_rate=float(data.get("frame_rate") or 30.0),
            reading_wpm=int(data.get("reading_wpm") or 155),
            notes=str(data.get("notes") or cls.notes),
        )


def load_timeline(path) -> Timeline:
    import json
    from pathlib import Path

    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return Timeline.from_dict(raw)
