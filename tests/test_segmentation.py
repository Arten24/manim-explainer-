from pathlib import Path

from quonitron_manim.subtitles.segment import (
    SegmentSettings,
    estimate_cue_duration,
    pack_cues,
    split_narration,
)


def test_split_respects_max_chars_and_protected_terms():
    narration = (
        "The variable name stays attached to the box. "
        "We then write a much longer sentence about how the programming language "
        "keeps that label for you even when the stored bits change underneath."
    )
    parts = split_narration(narration, SegmentSettings(max_chars=70))
    assert len(parts) >= 2
    assert all(len(p) <= 80 for p in parts)
    joined = " ".join(parts)
    assert "variable name" in joined
    assert "programming language" in joined


def test_pack_cues_assigns_stable_ids():
    texts = [
        "Imagine you are tidying a desk.",
        "A variable is a named place in memory.",
        "The name stays, and the value can change.",
    ]
    cues = pack_cues(texts, scene_id="demo")
    assert [c.id for c in cues] == ["cue-001", "cue-002", "cue-003"]
    again = pack_cues(texts, scene_id="demo")
    assert [c.id for c in again] == [c.id for c in cues]
    assert cues[0].end_time > cues[0].start_time
    assert cues[1].start_time >= cues[0].end_time - 1e-9


def test_durations_are_not_identical():
    short = estimate_cue_duration("It is the handle.", SegmentSettings())
    long = estimate_cue_duration(
        "We are opening the same box and replacing the note inside.",
        SegmentSettings(),
    )
    assert long > short


def test_demo_narration_segments_into_many_cues(repo_root: Path):
    text = (repo_root / "examples" / "variable_narration.txt").read_text(encoding="utf-8")
    parts = split_narration(text)
    assert 20 <= len(parts) <= 80
    assert parts[0].startswith("Imagine")
    assert parts[-1].endswith("value.")
    for part in parts:
        assert " " in part
