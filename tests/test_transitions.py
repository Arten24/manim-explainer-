from pathlib import Path

from quonitron_manim.core.catalog import search_catalog
from quonitron_manim.motion.base import MotionError
from quonitron_manim.timeline.models import (
    LinkedCue,
    SceneWindow,
    Timeline,
    VisualEvent,
    load_timeline,
)
from quonitron_manim.timeline.validate import validate_timeline
from quonitron_manim.transitions import ALL_TRANSITIONS, search_transitions
from quonitron_manim.transitions.simple import FadeTransition, SlideTransition, WipeTransition


def test_every_transition_validates_defaults():
    ids = []
    for cls in ALL_TRANSITIONS:
        recipe = cls()
        recipe.validate()
        assert recipe.component_id.startswith("transition.")
        assert recipe.category == "transition"
        assert recipe.manim_api
        assert recipe.run_time() > 0
        ids.append(recipe.component_id)
    assert len(ids) == len(set(ids))
    assert len(ids) >= 24


def test_search_transitions_filters():
    hits = search_transitions("wipe from left")
    assert any(cls.component_id == "transition.simple.wipe" for cls in hits)
    camera = search_transitions("zoom", camera=True)
    assert camera
    assert all(cls.needs_moving_camera for cls in camera)
    story = search_transitions("code to memory", subcategory="story")
    assert any(cls.component_id == "transition.story.code_to_memory" for cls in story)


def test_invalid_direction():
    try:
        SlideTransition(direction="SIDEWAYS").validate()
        raise AssertionError("expected MotionError")
    except MotionError:
        pass
    WipeTransition(direction="LEFT").validate()
    FadeTransition().validate()


def test_catalog_finds_transition_aliases(repo_root: Path):
    hits = search_catalog("wipe from left", root=repo_root)
    assert any(item["id"] == "transition.simple.wipe" for item in hits)
    morph = search_catalog("transform one object into another", root=repo_root)
    assert any(item["id"] == "transition.continuity.morph" for item in morph)


def test_beats_do_not_reset_the_clock(repo_root: Path):
    timeline = load_timeline(repo_root / "examples" / "journey_timeline.json")
    assert timeline.beats
    assert timeline.scene.duration >= 60
    assert timeline.scene.duration <= 90
    spanning = timeline.spanning_cues()
    assert spanning, "at least one caption should continue across a beat"
    # Same seconds clock: a cue after a beat change is later, not restarted at 0
    later = [c for c in timeline.cues if c.effective_start() > timeline.beats[0].end]
    assert later
    assert later[0].effective_start() > 1.0


def test_journey_timeline_validates(repo_root: Path):
    from quonitron_manim.motion import ALL_MOTION_RECIPES

    timeline = load_timeline(repo_root / "examples" / "journey_timeline.json")
    known = [cls.component_id for cls in ALL_MOTION_RECIPES] + [
        cls.component_id for cls in ALL_TRANSITIONS
    ]
    report = validate_timeline(timeline, known_motion_ids=known)
    assert report.ok, [item.message for item in report.errors]
    assert any(e.kind == "transition" for e in timeline.events)
    texts = " ".join(c.text for c in timeline.cues)
    assert "score" in texts
    assert all(c.text[:1].isupper() or c.text[:1].isdigit() for c in timeline.cues)


def test_unknown_transition_source_is_an_error():
    timeline = Timeline(
        scene=SceneWindow("s", 0, 8),
        events=[
            VisualEvent(
                "t1",
                "s",
                "transition.simple.fade",
                0,
                2,
                source_id="missing",
                destination_id="also-missing",
            )
        ],
        cues=[LinkedCue("c1", "s", 1, "A complete English sentence.", 0, 2, event_ids=["t1"])],
    )
    report = validate_timeline(
        timeline, known_motion_ids=["transition.simple.fade"]
    )
    assert report.errors
    assert any("source_id" in item.message for item in report.errors)


def test_wipe_overlapping_cue_is_a_warning():
    timeline = Timeline(
        scene=SceneWindow("s", 0, 6),
        events=[
            VisualEvent("t1", "s", "transition.simple.wipe", 0, 2, play_duration=1.0),
        ],
        cues=[LinkedCue("c1", "s", 1, "This caption sits under a wipe.", 0, 2, event_ids=["t1"])],
    )
    report = validate_timeline(
        timeline, known_motion_ids=["transition.simple.wipe"]
    )
    assert report.ok
    assert any("unreadable" in item.message for item in report.warnings)


def test_cue_may_use_a_beat_id():
    timeline = Timeline(
        scene=SceneWindow("program", 0, 10),
        beats=[SceneWindow("intro", 0, 4), SceneWindow("body", 4, 10)],
        events=[VisualEvent("t1", "intro", "transition.simple.fade", 0, 1)],
        cues=[
            LinkedCue("c1", "intro", 1, "We begin with a named box.", 0, 2, event_ids=["t1"]),
            LinkedCue("c2", "body", 2, "Then we keep the same clock running.", 4, 6),
        ],
    )
    report = validate_timeline(
        timeline, known_motion_ids=["transition.simple.fade"]
    )
    assert report.ok
