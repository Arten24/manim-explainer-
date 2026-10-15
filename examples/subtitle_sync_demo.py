"""Part 5: one canonical seconds timeline; no supplied narration recording.

manim -ql examples/subtitle_sync_demo.py SubtitleSyncDemo
Authoring/validation/export imports work without Manim.
"""
from pathlib import Path
from quonitron_manim.timeline import LinkedCue, SceneWindow, Timeline, VisualEvent
from quonitron_manim.subtitles.segment import cues_for_event


def build_timeline():
    events = [
        VisualEvent(id="reveal", scene_id="intro", motion_id="motion.appearance.fade_in", start=0, end=4, play_duration=0.5),
        VisualEvent(id="camera", scene_id="detail", motion_id="transition.camera.zoom_in", start=4, end=7, play_duration=1,
                    kind="transition", source_id="intro", destination_id="detail"),
        VisualEvent(id="recap", scene_id="detail", motion_id="motion.emphasis.indicate", start=7, end=11, play_duration=0.5),
    ]
    cues = cues_for_event("A variable gives a value a name.", events[0])
    # Deliberately spans the beat boundary and camera transition; no second clock.
    cues += [LinkedCue(id="camera-explanation", scene_id="sync", sequence=2,
        text="The view moves; the caption stays put.", start_time=3.8, end_time=7,
        event_ids=["camera"], timing_source="event_window")]
    cues[0].end_time = 3.6  # A deliberate silent gap, not synthetic speech alignment.
    cues += [LinkedCue(id="recap-explanation", scene_id="detail", sequence=3,
        text="The name points to the value.\nIt does not copy it.", start_time=7.2, end_time=10.5,
        event_ids=["recap"], timing_source="event_window")]
    return Timeline(scene=SceneWindow("sync", 0, 11),
        beats=[SceneWindow("intro", 0, 4), SceneWindow("detail", 4, 11)],
        events=events, cues=cues,
        notes="Estimated event-window timing; no narration recording supplied.",
        narration="\n".join(c.text for c in cues))


def export_demo(directory):
    from quonitron_manim.timeline.export_subtitles import write_timeline_subtitles
    from quonitron_manim.timeline.report import write_timeline_report
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    timeline = build_timeline()
    (directory / "subtitle_sync_timeline.json").write_text(
        __import__("json").dumps(timeline.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    result = write_timeline_subtitles(timeline, directory)
    write_timeline_report(timeline, directory / "subtitle_sync_report.md")
    return result


# Optional renderer imports do not prevent notebook authoring/export on light installs.
try:
    from quonitron_manim.core.base_scene import QuonitronMovingCameraScene
except ImportError:
    QuonitronMovingCameraScene = object


class SubtitleSyncDemo(QuonitronMovingCameraScene):
    def construct(self):
        from manim import DOWN, FadeIn, Indicate, VGroup
        from quonitron_manim.core.text import measured_text
        from quonitron_manim.components.foundation.subtitle_overlay import SubtitleOverlay
        from quonitron_manim.design.layout import place_in
        from quonitron_manim.timeline.player import play_on_scene
        title = measured_text("A name for a value", "heading", self.theme,
                              max_width=10, max_height=1.5)
        code = measured_text("score = 10", "body", self.theme, max_width=8, max_height=1)
        place_in(title, self.layout_validator.regions["content"])
        code.next_to(title, DOWN, buff=0.5)
        group = VGroup(title, code)
        self.register_layout("explanation", group)
        overlay = SubtitleOverlay(theme=self.theme)
        self.sync_timeline = build_timeline()
        self.sync_overlay = overlay
        play_on_scene(self, self.sync_timeline, {
            "reveal": lambda e: FadeIn(group),
            "camera": lambda e: self.camera.frame.animate.scale(0.92).shift([0.15, 0.1, 0]),
            "recap": lambda e: Indicate(code),
        }, overlay=overlay)
