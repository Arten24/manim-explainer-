from pathlib import Path

from quonitron_manim.subtitles import (
    SubtitleCue,
    SubtitleTrack,
    format_timestamp,
    load_track,
    to_srt,
    to_vtt,
    validate_track,
    write_srt,
    write_vtt,
)


def test_demo_track_loads_and_exports(repo_root, tmp_path: Path):
    track = load_track(repo_root / "examples" / "subtitle_demo.json")
    report = validate_track(track)
    assert report.ok, [item.message for item in report.errors]
    assert len(track.cues) >= 4
    for cue in track.cues:
        assert cue.text.endswith((".", "?", "!")) or "," in cue.text
        assert " " in cue.text
        assert cue.end_time > cue.start_time
    srt = to_srt(track)
    vtt = to_vtt(track)
    assert "Think of a variable as a labeled box" in srt
    assert srt.strip()[0].isdigit()
    assert "-->" in srt
    assert vtt.startswith("WEBVTT")
    assert "Estimated timings" in vtt
    write_srt(track, tmp_path / "demo.srt")
    write_vtt(track, tmp_path / "demo.vtt")
    assert (tmp_path / "demo.srt").read_text(encoding="utf-8") == srt


def test_timestamp_format():
    assert format_timestamp(0) == "00:00:00,000"
    assert format_timestamp(3661.5, vtt=True) == "01:01:01.500"


def test_end_time_must_follow_start():
    try:
        SubtitleCue("x", "s", 1, "Hello there, student.", 2.0, 1.0)
        raise AssertionError("expected ValueError")
    except ValueError as exc:
        assert "end_time" in str(exc)


def test_overlap_policy_error():
    track = SubtitleTrack(overlap_policy="error")
    track.add(
        SubtitleCue("a", "s", 1, "First complete sentence.", 0.0, 2.0)
    )
    track.add(
        SubtitleCue("b", "s", 2, "Second complete sentence.", 1.5, 3.0)
    )
    report = validate_track(track)
    assert not report.ok
    assert any("overlap" in item.message for item in report.errors)


def test_overlap_policy_warn_still_exports():
    track = SubtitleTrack(overlap_policy="warn")
    track.add(SubtitleCue("a", "s", 1, "First complete sentence.", 0.0, 2.0))
    track.add(SubtitleCue("b", "s", 2, "Second complete sentence.", 1.5, 3.5))
    report = validate_track(track)
    assert report.ok
    assert report.warnings
    text = to_srt(track)
    assert "First complete sentence." in text
