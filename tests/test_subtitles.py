from pathlib import Path

from quonitron.subtitles import (
    SubtitleCue,
    cues_from_sentences,
    format_timestamp,
    to_srt,
    to_vtt,
    write_srt,
    write_vtt,
)


def test_timestamp_srt_and_vtt():
    assert format_timestamp(0) == "00:00:00,000"
    assert format_timestamp(3661.5, vtt=True) == "01:01:01.500"


def test_cues_from_sentences_are_complete_lines():
    track = cues_from_sentences(
        [
            "Gradient descent walks downhill on a loss surface.",
            "Each step subtracts a scaled gradient from the current weights.",
        ],
        scene_id="scene_001",
        reading_wpm=160,
    )
    assert len(track.cues) == 2
    assert track.cues[0].text.endswith(".")
    assert track.cues[0].end_seconds > track.cues[0].start_seconds
    assert track.cues[1].start_seconds >= track.cues[0].end_seconds


def test_srt_and_vtt_export(tmp_path: Path):
    track = cues_from_sentences(
        ["This is a complete explanatory sentence."],
        "intro",
    )
    srt = to_srt(track)
    vtt = to_vtt(track)
    assert "00:00:00,000 -->" in srt
    assert srt.strip().startswith("1")
    assert vtt.startswith("WEBVTT")
    assert "This is a complete explanatory sentence." in srt
    srt_path = write_srt(track, tmp_path / "out.srt")
    vtt_path = write_vtt(track, tmp_path / "out.vtt")
    assert srt_path.read_text(encoding="utf-8") == srt
    assert vtt_path.read_text(encoding="utf-8") == vtt


def test_invalid_cue_rejected():
    try:
        SubtitleCue("s", 1, "Hello.", 2.0, 1.0)
        assert False, "expected ValueError"
    except ValueError:
        pass
