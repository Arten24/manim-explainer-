"""Part 5 canonical timing and export regressions; native checks are separate."""
import html
import math
import re
from dataclasses import replace

import pytest

from quonitron_manim.timeline import LinkedCue, SceneWindow, Timeline, VisualEvent
from quonitron_manim.timeline.validate import validate_timeline
from quonitron_manim.timeline.export_subtitles import timeline_to_track
from quonitron_manim.subtitles.export import to_srt, to_vtt, format_timestamp
from quonitron_manim.subtitles.models import SubtitleStyle
from quonitron_manim.subtitles.segment import SegmentSettings, cues_for_event


def cue(**kw):
    args = dict(id="cue-001", scene_id="s", sequence=1, text="A value has a name.",
                start_time=1., end_time=3.)
    args.update(kw)
    return LinkedCue(**args)


def timeline(cues=None, **kw):
    return Timeline(scene=SceneWindow("s", 0, 12), cues=cues if cues is not None else [cue()], **kw)


@pytest.mark.parametrize("start,end", [(math.nan, 2), (0, math.inf), (-1, 1), (2, 2), (2, 1)])
def test_reject_invalid_intervals(start, end):
    with pytest.raises(ValueError):
        cue(start_time=start, end_time=end)


@pytest.mark.parametrize("text", ["", " ", "a\x00b", "a\n\nb"])
def test_reject_bad_text(text):
    with pytest.raises(ValueError):
        cue(text=text)


@pytest.mark.parametrize("id", ["", "has space", "a-->b", "a\nb"])
def test_reject_bad_ids(id):
    with pytest.raises(ValueError):
        cue(id=id)


def test_alignment_provenance_and_effective_padding_roundtrip():
    c = cue(lead_in=.1, lead_out=.2)
    assert c.effective_start() == .9
    c.align(2, 4, notes="Aligned by editor")
    assert c.timing_status == "manually_aligned"
    assert c.effective_start() == 1.9 and c.effective_end() == 4.2
    with pytest.raises(ValueError, match="audio_reference"):
        c.align(2, 4, notes="reviewed", verified=True)
    assert c.timing_status == "manually_aligned"  # failed edits are atomic
    c.align(2, 4, notes="Reviewer listened to the recording", verified=True, audio_reference="narration.wav")
    t = timeline([c])
    loaded = Timeline.from_dict(t.to_dict())
    assert loaded.to_dict() == t.to_dict()
    exported = timeline_to_track(loaded).cues[0]
    assert exported.timing_status == "verified"
    assert exported.alignment_notes == c.alignment_notes
    assert exported.start_time == c.effective_start()


def test_mutations_links_and_duplicate_ids_are_validated():
    t = timeline()
    t.cues[0].end_time = math.nan
    assert validate_timeline(t).errors
    t = timeline([cue(), cue(sequence=2)])
    assert any("Duplicate cue" in x.message for x in validate_timeline(t).errors)
    t = timeline([cue(event_ids=["missing"])])
    assert validate_timeline(t).errors
    e = VisualEvent("event", "s", "motion", 0, 1, cue_ids=["missing"])
    assert validate_timeline(timeline([], events=[e])).errors


def test_nested_overlap_and_explicit_multispeaker():
    cues = [cue(end_time=10), cue(id="short", sequence=2, start_time=2, end_time=3),
            cue(id="nested", sequence=3, start_time=4, end_time=5)]
    report = validate_timeline(timeline(cues))
    assert len([i for i in report.errors if "overlap" in i.message]) == 2
    a, b = cue(speaker="A", overlap_ok=True), cue(id="other", sequence=2, speaker="B", overlap_ok=True)
    t = timeline([a, b], cue_overlap_policy="allow")
    assert not validate_timeline(t).errors
    assert [c.id for c in t.cues_at(2)] == ["cue-001", "other"]
    assert timeline_to_track(t).overlap_policy == "allow"
    b.speaker = "A"
    assert validate_timeline(t).errors


def test_half_open_gaps_and_event_estimates_deterministic():
    event = VisualEvent("reveal", "s", "motion", 2, 8)
    text = "A variable names a value. The name is not the value."
    first = cues_for_event(text, event, gap=.2)
    assert [c.to_dict() for c in first] == [c.to_dict() for c in cues_for_event(text, event, gap=.2)]
    assert all(c.timing_status == "estimated" and c.timing_source == "event_window" for c in first)
    assert first[0].effective_start() == 2 and first[-1].effective_end() == 8
    t = timeline(first, events=[event])
    assert not t.cues_at(0) and not t.cues_at(8)
    assert not t.cues_at(first[0].effective_end())
    assert not validate_timeline(t).errors
    with pytest.raises(ValueError):
        SegmentSettings(protected=[""])
    with pytest.raises(ValueError):
        cues_for_event(text, event, gap=100)


def test_export_sorted_unicode_literal_markup_multiline_and_precision():
    text = '“Name” → মান & <value>!\nSecond line.'
    t = timeline([cue(id="later", sequence=2, start_time=5, end_time=6), cue(text=text)])
    track = timeline_to_track(t)
    assert [c.id for c in track.cues] == ["cue-001", "later"]
    srt, vtt = to_srt(track), to_vtt(track)
    assert html.escape(text, quote=False) in srt and html.escape(text, quote=False) in vtt
    assert "00:00:01,000 --> 00:00:03,000" in srt
    assert "00:00:01.000 --> 00:00:03.000" in vtt
    assert track.cues[0].text == text
    tiny = timeline_to_track(timeline([cue(start_time=.0001, end_time=.0002)]))
    with pytest.raises(ValueError, match="millisecond"):
        to_srt(tiny)
    with pytest.raises(ValueError, match="millisecond"):
        to_vtt(tiny)
    with pytest.raises(ValueError):
        format_timestamp(float("inf"))
    assert format_timestamp(59.9996) == "00:01:00,000"
    assert to_srt(timeline_to_track(timeline([]))) == ""
    assert to_vtt(timeline_to_track(timeline([]))).startswith("WEBVTT")


def test_srt_parser_when_available():
    # Optional independent parser, not a library runtime dependency.
    try:
        import srt
    except ImportError:
        return  # structural timestamp assertions above always run
    parsed = list(srt.parse(to_srt(timeline_to_track(timeline()))))
    assert len(parsed) == 1 and parsed[0].start.total_seconds() == 1
    assert parsed[0].content == cue().text


def test_scene_clock_does_not_accumulate_frame_drift():
    from quonitron_manim.timeline.player import TimelineClock
    class Scene:
        time = 10.
    scene = Scene()
    clock = TimelineClock()
    clock.bind(scene, start=2)
    for _ in range(20):
        clock.sync(.1)
    assert clock.time == 2
    scene.time = 11.25
    assert clock.sync(.1) == 3.25


def test_style_stays_inside_shared_region_and_projection_uses_aabbs():
    from quonitron_manim.design.theme import get_theme
    from quonitron_manim.design.layout import LayoutItem, LayoutValidator, SafeArea
    from tests.test_layout_audit import Box
    style = SubtitleStyle(max_width=8, padding=.05)
    region = style.region(get_theme())
    assert region.width == 8 and region.height < 1.05
    validator = LayoutValidator({"content": SafeArea(-2, 2, -2, 2)})
    mob = Box(9, 11, 9, 11)
    assert not validator.validate([LayoutItem("moving", mob)], viewport=([10, 10, 0], 1))
    with pytest.raises(ValueError):
        SubtitleStyle(max_lines=0)


def test_demo_validation_and_exports(tmp_path):
    from examples.subtitle_sync_demo import build_timeline, export_demo
    t = build_timeline()
    assert not validate_timeline(t).errors
    assert all(c.timing_status == "estimated" for c in t.cues)
    assert any("crosses" in i.message or "spans" in i.message for i in validate_timeline(t).warnings)
    result = export_demo(tmp_path)
    assert result["srt"].read_text(encoding="utf-8") == result["srt_text"]


def test_nonzero_program_origin_and_optional_audio_share_elapsed_seconds():
    from quonitron_manim.timeline import NarrationAudio
    from quonitron_manim.timeline.player import play_on_scene
    class Scene:
        time = 100.
        calls = []
        def add_sound(self, path, time_offset):
            self.calls.append((path, time_offset, self.time))
        def wait(self, seconds):
            self.time += seconds
    t = Timeline(SceneWindow("offset", 5, 9), narration_audio=NarrationAudio("voice.wav", 6, 2))
    scene = Scene()
    clock = play_on_scene(scene, t, {})
    assert scene.time == 104 and clock.time == 9
    assert scene.calls == [("voice.wav", 1, 100)]
    assert Timeline.from_dict(t.to_dict()).narration_audio == t.narration_audio
    t.narration_audio.duration = 10
    assert validate_timeline(t).errors


def test_nested_visual_overlap_and_pause_overrun_are_rejected():
    events = [VisualEvent("long", "s", "motion", 0, 8),
              VisualEvent("inner1", "s", "motion", 1, 2),
              VisualEvent("inner2", "s", "motion", 4, 5)]
    report = validate_timeline(timeline([], events=events))
    assert len([i for i in report.errors if "overlapping play" in i.message]) == 2
    events = [VisualEvent("last", "s", "motion", 10, 12, pause_after=1)]
    assert any("exceeds scene end" in i.message for i in validate_timeline(timeline([], events=events)).errors)


def test_lead_times_and_invalid_status_are_not_silently_clamped():
    with pytest.raises(ValueError):
        cue(lead_in=2)
    with pytest.raises(ValueError):
        cue(lead_out=float("inf"))
    with pytest.raises(ValueError):
        cue(timing_status="aligned")
    t = timeline([cue(end_time=11.9, lead_out=.2)])
    assert validate_timeline(t).errors
    with pytest.raises(ValueError):
        timeline_to_track(t)
