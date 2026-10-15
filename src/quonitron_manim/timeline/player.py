"""Play a compiled timeline on a QuonitronScene.

Subtitles follow the same clock as visual events. The overlay updater uses
elapsed dt from Manim plays/waits, starting at 0 when playback begins.

Overlapping events (overlap_ok) are batched into AnimationGroup. Accidental
overlaps should already have failed validation.
"""

from __future__ import annotations

import math

from typing import Any, Callable, Dict, Optional

from quonitron_manim.timeline.models import Timeline, VisualEvent
from quonitron_manim.timeline.schedule import batch_events
from quonitron_manim.timeline.validate import validate_timeline


Binder = Callable[[VisualEvent], Any]


class TimelineClock:
    """Canonical seconds, bound to scene elapsed time when a renderer is present."""
    def __init__(self) -> None:
        self.time = 0.0
        self._scene = None
        self._origin = 0.0
        self._start = 0.0

    def bind(self, scene, *, start=0.0):
        self._scene = scene
        self._origin = float(getattr(scene, "time", 0.0))
        self._start = start
        self.time = start

    def sync(self, dt=0.0):
        if self._scene is not None and hasattr(self._scene, "time"):
            self.time = self._start + float(self._scene.time) - self._origin
        else:
            self.advance(dt)
        return self.time

    def advance(self, dt: float) -> None:
        if not math.isfinite(dt):
            raise ValueError("Clock delta must be finite")
        self.time += max(0.0, dt)


def play_on_scene(
    scene: Any,
    timeline: Timeline,
    binders: Dict[str, Binder],
    *,
    overlay: Optional[Any] = None,
    validate: bool = True,
) -> TimelineClock:
    if validate:
        validate_timeline(timeline).raise_if_invalid()
    missing = [event.id for event in timeline.events if event.id not in binders]
    if missing:
        raise KeyError(f"No binders for events: {missing}")

    clock = TimelineClock()
    clock.bind(scene, start=timeline.scene.start)
    if overlay is not None:
        overlay.attach(scene, timeline, clock)

    if timeline.narration_audio:
        scene.add_sound(timeline.narration_audio.path,
                        time_offset=timeline.narration_audio.start_time - timeline.scene.start)
    groups = batch_events(timeline.events)
    cursor = timeline.scene.start
    for group in groups:
        start = min(event.start for event in group)
        end = max(event.play_end() for event in group)
        gap = start - cursor
        if gap > 1e-6:
            scene.wait(gap)
        anims = []
        for event in group:
            delay = event.start - start
            anim = binders[event.id](event)
            if delay > 1e-6:
                from manim import Succession, Wait

                anims.append(Succession(Wait(delay), anim))
            else:
                anims.append(anim)
        run_time = end - start
        if len(anims) == 1:
            scene.play(anims[0], run_time=run_time)
        else:
            from manim import AnimationGroup

            scene.play(AnimationGroup(*anims), run_time=run_time)
        pause = max(event.pause_after for event in group)
        if pause > 1e-6:
            scene.wait(pause)
        cursor = end + pause

    tail = timeline.scene.end - cursor
    if tail > 1e-6:
        scene.wait(tail)
    clock.sync()
    # The playback boundary is exact even when frame quantization stops just short.
    clock.time = timeline.scene.end
    if overlay is not None:
        overlay.update_at(clock.time, scene=scene)
    return clock
