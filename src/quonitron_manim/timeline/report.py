"""Human-readable timeline inspection."""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import Union

from quonitron_manim.timeline.models import Timeline
from quonitron_manim.timeline.schedule import compile_schedule
from quonitron_manim.timeline.validate import TimelineReport, validate_timeline


def format_timeline_report(
    timeline: Timeline,
    *,
    validation: TimelineReport | None = None,
) -> str:
    buf = StringIO()
    scene = timeline.scene
    buf.write(f"# Timeline report — {scene.scene_id}\n\n")
    buf.write(f"- Title: {scene.title or '(untitled)'}\n")
    buf.write(
        f"- Scene window: {scene.start:.3f}s → {scene.end:.3f}s "
        f"({scene.duration:.3f}s)\n"
    )
    buf.write(
        f"- Frame rate: {timeline.frame_rate:g} fps "
        f"({timeline.seconds_to_frames(scene.duration)} frames in window)\n"
    )
    buf.write(f"- Reading speed: {timeline.reading_wpm} wpm (estimates only)\n")
    buf.write(f"- Events: {len(timeline.events)}\n")
    buf.write(f"- Cues: {len(timeline.cues)}\n")
    buf.write(f"- Beats: {len(timeline.beats)} (same clock; not a second timeline)\n")
    buf.write(f"- Notes: {timeline.notes}\n\n")

    if timeline.beats:
        buf.write("## Conceptual beats\n\n")
        buf.write("| id | title | start | end |\n| --- | --- | ---: | ---: |\n")
        for beat in timeline.beats:
            buf.write(
                f"| `{beat.scene_id}` | {beat.title or '—'} | "
                f"{beat.start:.3f} | {beat.end:.3f} |\n"
            )
        spanning = timeline.spanning_cues()
        buf.write("\nCues that continue across a beat boundary:\n\n")
        if spanning:
            for cue in spanning:
                buf.write(
                    f"- `{cue.id}` {cue.effective_start():.3f}–"
                    f"{cue.effective_end():.3f}: {cue.text}\n"
                )
        else:
            buf.write("- None.\n")
        buf.write("\n")

    if validation is None:
        validation = validate_timeline(timeline)
    buf.write("## Validation\n\n")
    buf.write("OK\n\n" if validation.ok else "FAILED\n\n")
    for issue in validation.issues:
        buf.write(f"- **{issue.level}** `{issue.ref_id or '-'}` {issue.message}\n")
    if not validation.issues:
        buf.write("- No issues.\n")
    buf.write("\n## Visual events\n\n")
    buf.write("| id | kind | motion | start | end | play | src | dest |\n")
    buf.write("| --- | --- | --- | ---: | ---: | ---: | --- | --- |\n")
    for event in sorted(timeline.events, key=lambda item: item.start):
        buf.write(
            f"| `{event.id}` | {event.kind} | `{event.motion_id}` | {event.start:.3f} | "
            f"{event.end:.3f} | {event.animation_duration():.3f} | "
            f"{event.source_id or '—'} | {event.destination_id or '—'} |\n"
        )
    buf.write("\n## Subtitle cues\n\n")
    buf.write("| id | seq | status | start | end | event_ids | text |\n")
    buf.write("| --- | ---: | --- | ---: | ---: | --- | --- |\n")
    for cue in sorted(timeline.cues, key=lambda item: item.sequence):
        text = cue.text.replace("|", "/")
        buf.write(
            f"| `{cue.id}` | {cue.sequence} | {cue.timing_status} | "
            f"{cue.effective_start():.3f} | {cue.effective_end():.3f} | "
            f"{', '.join(cue.event_ids) or '—'} | {text} |\n"
        )
    buf.write("\n## Compiled schedule\n\n")
    for item in compile_schedule(timeline):
        buf.write(
            f"- t={item.time:7.3f}s  {item.kind:12}  {item.ref_id}  {item.payload}\n"
        )
    buf.write("\n## Narration (source of truth)\n\n")
    buf.write(timeline.narration.strip() + "\n")
    return buf.getvalue()


def write_timeline_report(timeline: Timeline, path: Union[str, Path]) -> Path:
    path = Path(path)
    path.write_text(format_timeline_report(timeline), encoding="utf-8")
    return path
