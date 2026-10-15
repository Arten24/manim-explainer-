"""Validate a shared timeline without rendering."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Sequence

from quonitron_manim.timeline.models import Timeline


@dataclass
class TimelineIssue:
    level: str
    message: str
    ref_id: Optional[str] = None


@dataclass
class TimelineReport:
    issues: List[TimelineIssue] = field(default_factory=list)

    @property
    def errors(self) -> List[TimelineIssue]:
        return [item for item in self.issues if item.level == "error"]

    @property
    def warnings(self) -> List[TimelineIssue]:
        return [item for item in self.issues if item.level == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def raise_if_invalid(self) -> None:
        if self.errors:
            raise ValueError("; ".join(item.message for item in self.errors))


def validate_timeline(
    timeline: Timeline,
    *,
    known_motion_ids: Optional[Sequence[str]] = None,
) -> TimelineReport:
    report = TimelineReport()
    scene = timeline.scene
    event_ids = [event.id for event in timeline.events]
    if len(event_ids) != len(set(event_ids)):
        report.issues.append(TimelineIssue("error", "Duplicate visual event ids"))
    cue_ids = [cue.id for cue in timeline.cues]
    if len(cue_ids) != len(set(cue_ids)):
        report.issues.append(TimelineIssue("error", "Duplicate cue ids"))

    known_events = set(event_ids)
    known_motions = set(known_motion_ids) if known_motion_ids is not None else None

    for event in timeline.events:
        if event.scene_id != scene.scene_id:
            report.issues.append(
                TimelineIssue(
                    "error",
                    f"{event.id}: scene_id {event.scene_id!r} != {scene.scene_id!r}",
                    event.id,
                )
            )
        if not scene.contains(event.start, event.end):
            report.issues.append(
                TimelineIssue(
                    "error",
                    f"{event.id}: interval {event.start:.3f}-{event.end:.3f} "
                    f"is outside scene {scene.start:.3f}-{scene.end:.3f}",
                    event.id,
                )
            )
        if known_motions is not None and event.motion_id not in known_motions:
            report.issues.append(
                TimelineIssue(
                    "error",
                    f"{event.id}: unknown motion_id {event.motion_id!r}",
                    event.id,
                )
            )
        for dep in event.depends_on:
            if dep not in known_events:
                report.issues.append(
                    TimelineIssue(
                        "error",
                        f"{event.id}: depends_on unknown event {dep!r}",
                        event.id,
                    )
                )
            elif dep == event.id:
                report.issues.append(
                    TimelineIssue("error", f"{event.id}: depends on itself", event.id)
                )
            else:
                prior = next(item for item in timeline.events if item.id == dep)
                if prior.play_end() - 1e-6 > event.start and not event.overlap_ok:
                    report.issues.append(
                        TimelineIssue(
                            "error",
                            f"{event.id}: depends on {dep} whose play window still runs "
                            f"until {prior.play_end():.3f}, after this start {event.start:.3f}",
                            event.id,
                        )
                    )

    ordered = sorted(timeline.events, key=lambda item: (item.start, item.id))
    for left, right in zip(ordered, ordered[1:]):
        # Accidental overlap is about *playback* windows, not semantic presence.
        if right.start < left.play_end() - 1e-6:
            allowed = left.overlap_ok or right.overlap_ok
            message = (
                f"Events {left.id} and {right.id} have overlapping play windows "
                f"({left.play_end():.3f} > {right.start:.3f})"
            )
            if allowed:
                report.issues.append(TimelineIssue("warning", message + " (intentional)", right.id))
            else:
                report.issues.append(TimelineIssue("error", message + " (accidental)", right.id))

    for cue in timeline.cues:
        if cue.scene_id != scene.scene_id:
            report.issues.append(
                TimelineIssue(
                    "error",
                    f"{cue.id}: scene_id {cue.scene_id!r} != {scene.scene_id!r}",
                    cue.id,
                )
            )
        start, end = cue.effective_start(), cue.effective_end()
        if not scene.contains(start, end):
            report.issues.append(
                TimelineIssue(
                    "error",
                    f"{cue.id}: effective interval {start:.3f}-{end:.3f} "
                    f"is outside the scene",
                    cue.id,
                )
            )
        if not cue.event_ids:
            report.issues.append(
                TimelineIssue(
                    "warning",
                    f"{cue.id}: no event_ids (narration is not linked to a visual)",
                    cue.id,
                )
            )
        for event_id in cue.event_ids:
            if event_id not in known_events:
                report.issues.append(
                    TimelineIssue(
                        "error",
                        f"{cue.id}: event_ids references unknown event {event_id!r}",
                        cue.id,
                    )
                )
            else:
                event = timeline.event_by_id(event_id)
                # A cue may span several events or sit beside a longer animation.
                # Warn only when the cue does not overlap the event at all.
                overlap = min(end, event.end) - max(start, event.start)
                if overlap <= 0:
                    report.issues.append(
                        TimelineIssue(
                            "warning",
                            f"{cue.id}: does not overlap linked event {event_id}",
                            cue.id,
                        )
                    )

    cue_ordered = sorted(timeline.cues, key=lambda item: (item.effective_start(), item.sequence))
    for left, right in zip(cue_ordered, cue_ordered[1:]):
        if right.effective_start() + 1e-6 < left.effective_end():
            report.issues.append(
                TimelineIssue(
                    "error",
                    f"Cues {left.id} and {right.id} overlap on the shared clock",
                    right.id,
                )
            )
    return report
