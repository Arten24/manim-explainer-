"""Cross-example validation adapted from branch adb921d; no renderer required."""
import json
from pathlib import Path

import pytest

from quonitron_manim.components.text import ALL_TEXT_COMPONENTS
from quonitron_manim.motion import ALL_MOTION_RECIPES
from quonitron_manim.subtitles.export import load_track, to_srt, to_vtt, write_srt, write_vtt
from quonitron_manim.subtitles.validation import validate_track
from quonitron_manim.timeline.export_subtitles import timeline_to_track
from quonitron_manim.timeline.models import load_timeline
from quonitron_manim.timeline.validate import validate_timeline
from quonitron_manim.transitions import ALL_TRANSITIONS


EXAMPLE_TIMELINES = sorted(
    path.name for path in Path(__file__).parents[1].glob("examples/*_timeline.json")
)
# Part 4 intentionally uses text component IDs as timeline actions in motion_id.
KNOWN_TIMELINE_ACTION_IDS = [
    component.component_id
    for component in ALL_MOTION_RECIPES + ALL_TRANSITIONS + ALL_TEXT_COMPONENTS
]


@pytest.mark.parametrize("filename", EXAMPLE_TIMELINES)
def test_example_timeline_validation_and_subtitle_exports(repo_root, tmp_path, filename):
    path = repo_root / "examples" / filename
    json.loads(path.read_text(encoding="utf-8"))
    timeline = load_timeline(path)
    report = validate_timeline(timeline, known_motion_ids=KNOWN_TIMELINE_ACTION_IDS)
    assert report.ok, [issue.message for issue in report.errors]

    track = timeline_to_track(timeline)
    subtitle_report = validate_track(track)
    assert subtitle_report.ok, [issue.message for issue in subtitle_report.errors]

    srt_path = write_srt(track, tmp_path / f"{timeline.scene.scene_id}.srt")
    vtt_path = write_vtt(track, tmp_path / f"{timeline.scene.scene_id}.vtt")
    assert srt_path.read_text(encoding="utf-8") == to_srt(track)
    assert vtt_path.read_text(encoding="utf-8") == to_vtt(track)
    assert srt_path.read_text(encoding="utf-8").strip()
    assert vtt_path.read_text(encoding="utf-8").startswith("WEBVTT")


def test_subtitle_json_demo_validates_and_exports(repo_root, tmp_path):
    track = load_track(repo_root / "examples" / "subtitle_demo.json")
    report = validate_track(track)
    assert report.ok, [issue.message for issue in report.errors]

    srt_path = write_srt(track, tmp_path / "subtitle_demo.srt")
    vtt_path = write_vtt(track, tmp_path / "subtitle_demo.vtt")
    assert srt_path.read_text(encoding="utf-8") == to_srt(track)
    assert vtt_path.read_text(encoding="utf-8") == to_vtt(track)
    assert vtt_path.read_text(encoding="utf-8").startswith("WEBVTT")
