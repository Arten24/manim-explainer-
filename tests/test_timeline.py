from pathlib import Path

from quonitron_manim.motion import ALL_MOTION_RECIPES
from quonitron_manim.subtitles import to_srt, to_vtt
from quonitron_manim.timeline.export_subtitles import timeline_to_track
from quonitron_manim.timeline.models import (
    LinkedCue,
    SceneWindow,
    Timeline,
    VisualEvent,
    load_timeline,
)
from quonitron_manim.timeline.schedule import compile_schedule, subtitle_states
from quonitron_manim.timeline.validate import validate_timeline


def _known():
    return [cls.component_id for cls in ALL_MOTION_RECIPES]


def test_demo_timeline_is_valid(repo_root: Path):
    timeline = load_timeline(repo_root / "examples" / "variable_timeline.json")
    report = validate_timeline(timeline, known_motion_ids=_known())
    assert report.ok, [item.message for item in report.errors]
    assert len(timeline.cues) >= 30
    assert timeline.scene.duration >= 60
    assert timeline.narration.strip()
    for cue in timeline.cues:
        assert cue.event_ids
        assert cue.timing_status == "estimated"
        assert cue.scene_id == timeline.scene.scene_id


def test_cue_ids_stable_when_timing_overridden(repo_root: Path):
    timeline = load_timeline(repo_root / "examples" / "variable_timeline.json")
    original = [(cue.id, cue.text) for cue in timeline.cues]
    timeline.override_cue("cue-001", 0.15, 2.4)
    assert timeline.cue_by_id("cue-001").timing_status == "manual"
    assert [(cue.id, cue.text) for cue in timeline.cues] == original
    assert timeline.cue_by_id("cue-001").effective_start() == 0.15


def test_missing_event_reference_is_an_error():
    timeline = Timeline(
        scene=SceneWindow("s", 0, 10),
        events=[
            VisualEvent("ev", "s", "motion.appearance.fade_in", 0, 1),
        ],
        cues=[
            LinkedCue("c1", "s", 1, "Hello there, learner.", 0, 2, event_ids=["nope"]),
        ],
    )
    report = validate_timeline(timeline, known_motion_ids=_known())
    assert not report.ok
    assert any("unknown event" in item.message for item in report.errors)


def test_cue_outside_scene_is_an_error():
    timeline = Timeline(
        scene=SceneWindow("s", 0, 5),
        events=[VisualEvent("ev", "s", "motion.appearance.fade_in", 0, 1)],
        cues=[LinkedCue("c1", "s", 1, "This cue overruns the scene window.", 0, 6, event_ids=["ev"])],
    )
    report = validate_timeline(timeline, known_motion_ids=_known())
    assert any("outside the scene" in item.message for item in report.errors)


def test_accidental_versus_intentional_play_overlap():
    accidental = Timeline(
        scene=SceneWindow("s", 0, 10),
        events=[
            VisualEvent("a", "s", "motion.appearance.fade_in", 0, 2, play_duration=2),
            VisualEvent("b", "s", "motion.appearance.fade_out", 1, 3, play_duration=2),
        ],
        cues=[LinkedCue("c1", "s", 1, "Two motions collide by accident.", 0, 2, event_ids=["a"])],
    )
    report = validate_timeline(accidental, known_motion_ids=_known())
    assert any("accidental" in item.message for item in report.errors)

    intentional = Timeline(
        scene=SceneWindow("s", 0, 10),
        events=[
            VisualEvent("a", "s", "motion.appearance.fade_in", 0, 2, play_duration=2, overlap_ok=True),
            VisualEvent("b", "s", "motion.appearance.fade_out", 1, 3, play_duration=2, overlap_ok=True),
        ],
        cues=[LinkedCue("c1", "s", 1, "Two motions overlap on purpose.", 0, 2, event_ids=["a", "b"])],
    )
    report = validate_timeline(intentional, known_motion_ids=_known())
    assert report.ok
    assert any("intentional" in item.message for item in report.warnings)


def test_wrong_scene_id_on_cue():
    timeline = Timeline(
        scene=SceneWindow("alpha", 0, 5),
        events=[VisualEvent("ev", "alpha", "motion.appearance.fade_in", 0, 1)],
        cues=[LinkedCue("c1", "beta", 1, "This belongs to another scene.", 0, 1, event_ids=["ev"])],
    )
    report = validate_timeline(timeline, known_motion_ids=_known())
    assert any("scene_id" in item.message for item in report.errors)


def test_duration_change_real():
    timeline = Timeline(
        scene=SceneWindow("s", 0, 12),
        events=[
            VisualEvent("a", "s", "motion.appearance.fade_in", 0, 2, play_duration=1),
            VisualEvent("b", "s", "motion.appearance.fade_out", 4, 6, play_duration=1),
        ],
        cues=[
            LinkedCue("c1", "s", 1, "First sentence stays put.", 0, 1.5, event_ids=["a"]),
            LinkedCue("c2", "s", 2, "Second sentence should shift.", 4, 6, event_ids=["b"]),
        ],
    )
    timeline.rescale_event("a", new_duration=3.0, shift_following=True)
    assert timeline.event_by_id("a").duration == 3.0
    assert abs(timeline.event_by_id("b").start - 5.0) < 1e-9
    assert abs(timeline.cue_by_id("c2").start_time - 5.0) < 1e-9


def test_frame_rate_conversion():
    timeline = Timeline(scene=SceneWindow("s", 0, 2), frame_rate=15)
    assert timeline.seconds_to_frames(1.0) == 15
    assert abs(timeline.frames_to_seconds(15) - 1.0) < 1e-9
    assert timeline.seconds_to_frames(0.2) == 3


def test_cue_at_and_schedule_match(repo_root: Path):
    timeline = load_timeline(repo_root / "examples" / "variable_timeline.json")
    first = timeline.cues[0]
    assert timeline.cue_at(first.effective_start() + 0.01).id == first.id
    assert timeline.cue_at(first.effective_end() + 0.01).id != first.id
    items = compile_schedule(timeline)
    kinds = {item.kind for item in items}
    assert "cue_start" in kinds and "event_start" in kinds
    mid = first.effective_start() + first.duration / 2
    states = subtitle_states(timeline, [mid])
    assert states == [first.id]


def test_srt_vtt_use_effective_times(repo_root: Path):
    timeline = load_timeline(repo_root / "examples" / "variable_timeline.json")
    track = timeline_to_track(timeline)
    srt = to_srt(track)
    vtt = to_vtt(track)
    assert "Imagine you are tidying a desk." in srt
    assert vtt.startswith("WEBVTT")
    assert str(len(timeline.cues)) in srt.splitlines()[0] or srt.strip()[0].isdigit()
    assert "cue-001" in vtt
