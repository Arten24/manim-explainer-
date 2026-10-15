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
    # Dataclasses remain editable for compatibility; validate mutations too.
    for obj in [timeline, timeline.scene, *timeline.beats, *timeline.events, *timeline.cues]:
        try:
            obj.__post_init__()
        except (ValueError, TypeError) as exc:
            report.issues.append(TimelineIssue("error", str(exc), getattr(obj, "id", None)))
    if report.errors:
        return report
    scene = timeline.scene
    event_ids = [event.id for event in timeline.events]
    if len(event_ids) != len(set(event_ids)):
        report.issues.append(TimelineIssue("error", "Duplicate visual event ids"))
    cue_ids = [cue.id for cue in timeline.cues]
    if len(cue_ids) != len(set(cue_ids)):
        report.issues.append(TimelineIssue("error", "Duplicate cue ids"))

    beat_ids = [b.scene_id for b in timeline.beats]
    if len(set(beat_ids)) != len(beat_ids) or timeline.scene.scene_id in beat_ids:
        report.issues.append(TimelineIssue("error", "Beat IDs must be unique and distinct from program ID"))
    if timeline.narration_audio:
        try:
            timeline.narration_audio.__post_init__()
            audio = timeline.narration_audio
            if audio.start_time < timeline.scene.start or audio.start_time >= timeline.scene.end:
                raise ValueError("Narration audio starts outside scene")
            if audio.duration is not None and audio.start_time + audio.duration > timeline.scene.end + 1e-6:
                raise ValueError("Narration audio duration exceeds scene")
        except (ValueError, TypeError) as exc:
            report.issues.append(TimelineIssue("error", str(exc)))
    known_events = set(event_ids)
    known_motions = set(known_motion_ids) if known_motion_ids is not None else None
    allowed_scenes = set(timeline.allowed_scene_ids())
    hiding = {
        "transition.simple.wipe",
        "transition.simple.cover",
    }

    for beat in timeline.beats:
        if not scene.contains(beat.start, beat.end):
            report.issues.append(
                TimelineIssue(
                    "error",
                    f"beat {beat.scene_id}: {beat.start:.3f}-{beat.end:.3f} "
                    f"is outside the program window",
                    beat.scene_id,
                )
            )

    for event in timeline.events:
        if event.scene_id not in allowed_scenes:
            report.issues.append(
                TimelineIssue(
                    "error",
                    f"{event.id}: scene_id {event.scene_id!r} is not the program "
                    f"or a declared beat. Known: {sorted(allowed_scenes)}",
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
        if event.kind == "transition":
            for ref, label in (
                (event.source_id, "source_id"),
                (event.destination_id, "destination_id"),
            ):
                if not ref:
                    continue
                if ref not in known_events and ref not in allowed_scenes:
                    report.issues.append(
                        TimelineIssue(
                            "error",
                            f"{event.id}: {label} {ref!r} is not an event or beat id",
                            event.id,
                        )
                    )
        if event.play_end() + event.pause_after > scene.end + 1e-6:
            report.issues.append(TimelineIssue("error", f"{event.id}: play/pause exceeds scene end", event.id))
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
    for index, left in enumerate(ordered):
        for right in ordered[index + 1:]:
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
        if cue.scene_id not in allowed_scenes:
            report.issues.append(
                TimelineIssue(
                    "error",
                    f"{cue.id}: scene_id {cue.scene_id!r} is not the program "
                    f"or a declared beat",
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

    sequences = [cue.sequence for cue in timeline.cues]
    if len(set(sequences)) != len(sequences):
        report.issues.append(TimelineIssue("error", "Cue sequence numbers must be unique"))
    cue_ordered = sorted(timeline.cues, key=lambda item: (item.effective_start(), item.sequence))
    if list(timeline.cues) != cue_ordered:
        report.issues.append(TimelineIssue("warning", "Cues are not in chronological order; playback/export sort canonically"))
    for index, left in enumerate(cue_ordered):
        for right in cue_ordered[index + 1:]:
            if right.effective_start() >= left.effective_end() - 1e-9:
                break
            allowed = (timeline.cue_overlap_policy == "allow" and left.overlap_ok and right.overlap_ok
                       and left.speaker and right.speaker and left.speaker != right.speaker)
            report.issues.append(TimelineIssue("warning" if allowed else "error",
                f"Cues {left.id} and {right.id} overlap on the shared clock"
                + (" (explicit distinct-speaker overlap)" if allowed else " (not explicitly permitted)"), right.id))
    for event in timeline.events:
        for cue_id in event.cue_ids:
            if cue_id not in set(cue_ids):
                report.issues.append(TimelineIssue("error", f"{event.id}: unknown cue_ids reference {cue_id}", event.id))
    # A pause occupies real playback time, and must not silently push later events.
    for group_index, left in enumerate(ordered):
        for right in ordered[group_index + 1:]:
            if left.play_end() <= right.start < left.play_end() + left.pause_after - 1e-6:
                report.issues.append(TimelineIssue("error", f"{left.id}: pause_after overlaps event {right.id}", left.id))

    for cue in timeline.spanning_cues():
        report.issues.append(
            TimelineIssue(
                "warning",
                f"{cue.id}: spans more than one conceptual beat "
                "(allowed — the clock does not reset at a scene change)",
                cue.id,
            )
        )

    for event in timeline.events:
        if event.motion_id not in hiding:
            continue
        play_start, play_end = event.start, event.play_end()
        for cue in timeline.cues:
            overlap = min(cue.effective_end(), play_end) - max(
                cue.effective_start(), play_start
            )
            if overlap > 0.15:
                report.issues.append(
                    TimelineIssue(
                        "warning",
                        f"{cue.id}: overlaps hiding transition {event.id} "
                        f"({overlap:.2f}s may be unreadable)",
                        cue.id,
                    )
                )
    return report
