"""Export SRT/VTT from the same timeline used for on-screen captions."""

from __future__ import annotations

from pathlib import Path
from typing import Union

from quonitron_manim.subtitles.export import to_srt, to_vtt, write_srt, write_vtt
from quonitron_manim.subtitles.models import SubtitleCue, SubtitleTrack
from quonitron_manim.timeline.models import Timeline


def timeline_to_track(timeline: Timeline) -> SubtitleTrack:
    from quonitron_manim.timeline.validate import validate_timeline
    validate_timeline(timeline).raise_if_invalid()
    track = SubtitleTrack(
        reading_wpm=timeline.reading_wpm,
        notes=timeline.notes,
        overlap_policy=timeline.cue_overlap_policy,
        preserve_lines=True,
    )
    for cue in sorted(timeline.cues, key=lambda c: (c.effective_start(), c.sequence, c.id)):
        track.add(
            SubtitleCue(
                id=cue.id,
                scene_id=cue.scene_id,
                sequence=cue.sequence,
                text=cue.text,
                start_time=cue.effective_start(),
                end_time=cue.effective_end(),
                visual_cue=cue.visual_cue,
                speaker=cue.speaker,
                event_ids=list(cue.event_ids), timing_status=cue.timing_status,
                timing_source=cue.timing_source, alignment_notes=cue.alignment_notes,
                narration_metadata=dict(cue.narration_metadata),
            )
        )
    return track


def write_timeline_subtitles(timeline: Timeline, dest_dir: Union[str, Path]) -> dict:
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    track = timeline_to_track(timeline)
    srt = dest / f"{timeline.scene.scene_id}.srt"
    vtt = dest / f"{timeline.scene.scene_id}.vtt"
    write_srt(track, srt)
    write_vtt(track, vtt)
    return {"srt": srt, "vtt": vtt, "track": track, "srt_text": to_srt(track), "vtt_text": to_vtt(track)}
