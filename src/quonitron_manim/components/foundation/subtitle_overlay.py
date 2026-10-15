"""On-screen subtitle overlay driven by the shared timeline.

Styling comes from the theme. Timing comes only from Timeline.cues_at().
"""

from __future__ import annotations

from typing import Any, Optional

from quonitron_manim.core.component import Component, register_component
from quonitron_manim.timeline.models import Timeline
from quonitron_manim.timeline.player import TimelineClock


@register_component
class SubtitleOverlay(Component):
    """Bottom-safe caption that follows timeline cues."""

    component_id = "foundation.subtitle_overlay"
    name = "Subtitle Overlay"
    category = "foundation"
    version = "0.3.0"

    def __init__(self, theme=None, **params: Any) -> None:
        super().__init__(theme=theme, **params)
        self._mob: Any = None
        self._shown_id: Optional[str] = None
        self.timeline: Optional[Timeline] = None
        self.clock: Optional[TimelineClock] = None
        from quonitron_manim.subtitles.models import SubtitleStyle
        self.style = self.param("style", None) or SubtitleStyle()
        self._preflight_cache = {}
        self._projection_scale = 1.0
        self._projection_center = (0.0, 0.0, 0.0)

    def build(self) -> Any:
        from quonitron_manim.core.text import subtitle_text

        self._canonical = subtitle_text(self.param("text", " "), self.theme, style=self.style)
        self._mob = self._canonical.copy()
        return self._mob

    def _restyle(self, text: str) -> None:
        from quonitron_manim.core.text import subtitle_text

        self._canonical = self._preflight_cache.get(text)
        if self._canonical is None:
            self._canonical = subtitle_text(text, self.theme, style=self.style)
        self._mob.become(self._canonical)
        # Cue replacement is canonical again, not in the previous camera pose.
        self._projection_scale = 1.0
        self._projection_center = (0.0, 0.0, 0.0)

    def _follow_viewport(self, scene: Any) -> None:
        """Apply only the change in camera pose; never deepcopy glyphs per frame.

        This is algebraically the same canonical-to-viewport transform as before,
        but a static camera does no work and moving frames touch only point arrays.
        """
        frame = getattr(getattr(scene, "camera", None), "frame", None)
        if frame is None:
            return
        scale = float(frame.width) / self.theme.frame_width
        center = tuple(float(value) for value in frame.get_center())
        if (abs(scale - self._projection_scale) <= 1e-12
                and all(abs(a - b) <= 1e-12 for a, b in zip(center, self._projection_center))):
            return
        self._mob.shift([-value for value in self._projection_center])
        self._mob.scale(scale / self._projection_scale, about_point=[0, 0, 0])
        self._mob.shift(center)
        self._projection_scale = scale
        self._projection_center = center

    def show_text(self, text: str) -> None:
        if self._mob is None:
            self.get()
        self._restyle(text)

    def _active_text(self, cues):
        return "\n".join((f"{c.speaker}: " if self.style.speaker_labels and c.speaker else "") + c.text
                         for c in cues) or " "

    def preflight(self, timeline):
        """Measure every active combination (including simultaneous speakers) once."""
        from quonitron_manim.timeline.validate import validate_timeline
        from quonitron_manim.core.text import subtitle_text
        validate_timeline(timeline).raise_if_invalid()
        times = {timeline.scene.start, *(c.effective_start() for c in timeline.cues),
                 *(c.effective_end() for c in timeline.cues)}
        self._preflight_cache = {}
        for time in sorted(times):
            text = self._active_text(timeline.cues_at(time))
            if text not in self._preflight_cache:
                self._preflight_cache[text] = subtitle_text(text, self.theme, style=self.style)
        return {text: mob.measured_line_count for text, mob in self._preflight_cache.items()}

    def update_at(self, time, *, scene=None):
        cues = self.timeline.cues_at(time)
        ids = tuple(c.id for c in cues)
        changed = ids != self._shown_id
        if changed:
            self._shown_id = ids
            self.show_text(self._active_text(cues))
        previous = (self._projection_scale, self._projection_center)
        if scene is not None:
            self._follow_viewport(scene)
            moving = previous != (self._projection_scale, self._projection_center)
            # Shared collision diagnostics, without glyph deepcopy on moving frames.
            if (changed or moving) and hasattr(scene, "check_layout"):
                scene.check_layout()
        return ids

    def attach(self, scene: Any, timeline: Timeline, clock: TimelineClock) -> Any:
        self.preflight(timeline)
        self.timeline = timeline
        self.clock = clock
        mob = self.get()
        scene.add(mob)
        if hasattr(scene, "register_layout"):
            scene.register_layout("subtitle", mob, region="subtitle")

        def _tick(_mobject: Any, dt: float) -> None:
            self.update_at(clock.sync(dt), scene=scene)

        mob.add_updater(_tick)
        self.update_at(clock.time, scene=scene)
        return mob
