"""Compile a timeline into an inspectable playback schedule."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Sequence

from quonitron_manim.timeline.models import Timeline, VisualEvent


@dataclass(frozen=True)
class ScheduleItem:
    time: float
    kind: str
    ref_id: str
    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def compile_schedule(timeline: Timeline) -> List[ScheduleItem]:
    """Return cue and event markers sorted by time, then kind."""
    items: List[ScheduleItem] = []
    for event in timeline.events:
        items.append(
            ScheduleItem(
                time=event.start,
                kind="event_start",
                ref_id=event.id,
                payload={
                    "motion_id": event.motion_id,
                    "end": event.end,
                    "run_time": event.animation_duration(),
                    "play_end": event.play_end(),
                    "label": event.label,
                },
            )
        )
        items.append(
            ScheduleItem(
                time=event.end,
                kind="event_end",
                ref_id=event.id,
                payload={"motion_id": event.motion_id},
            )
        )
        if event.pause_after > 0:
            items.append(
                ScheduleItem(
                    time=event.end,
                    kind="pause",
                    ref_id=event.id,
                    payload={"duration": event.pause_after},
                )
            )
    for cue in timeline.cues:
        items.append(
            ScheduleItem(
                time=cue.effective_start(),
                kind="cue_start",
                ref_id=cue.id,
                payload={"text": cue.text, "end": cue.effective_end()},
            )
        )
        items.append(
            ScheduleItem(
                time=cue.effective_end(),
                kind="cue_end",
                ref_id=cue.id,
                payload={},
            )
        )
    kind_order = {
        "cue_end": 0,
        "event_end": 1,
        "pause": 2,
        "event_start": 3,
        "cue_start": 4,
    }
    items.sort(key=lambda item: (item.time, kind_order.get(item.kind, 9), item.ref_id))
    return items


def batch_events(events: Sequence[VisualEvent]) -> List[List[VisualEvent]]:
    """Group events whose *play* windows overlap (not the semantic interval)."""
    ordered = sorted(events, key=lambda item: (item.start, item.id))
    groups: List[List[VisualEvent]] = []
    for event in ordered:
        if not groups:
            groups.append([event])
            continue
        current = groups[-1]
        window_end = max(item.play_end() for item in current)
        if event.start < window_end - 1e-6:
            current.append(event)
        else:
            groups.append([event])
    return groups


def subtitle_states(timeline: Timeline, times: Sequence[float]) -> List[Optional[str]]:
    from typing import Optional

    return [
        (timeline.cue_at(t).id if timeline.cue_at(t) is not None else None) for t in times
    ]
