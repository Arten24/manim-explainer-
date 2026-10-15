"""On-screen subtitle overlay driven by the shared timeline.

Styling comes from the theme. Timing comes only from Timeline.cue_at().
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
        self._projection_scale = 1.0
        self._projection_center = (0.0, 0.0, 0.0)

    def build(self) -> Any:
        from quonitron_manim.core.text import subtitle_text

        self._canonical = subtitle_text(self.param("text", " "), self.theme)
        self._mob = self._canonical.copy()
        return self._mob

    def _restyle(self, text: str) -> None:
        from quonitron_manim.core.text import subtitle_text

        self._canonical = subtitle_text(text, self.theme)
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

    def attach(self, scene: Any, timeline: Timeline, clock: TimelineClock) -> Any:
        self.timeline = timeline
        self.clock = clock
        mob = self.get()
        scene.add(mob)
        if hasattr(scene, "register_layout"):
            scene.register_layout("subtitle", mob, region="subtitle")
        overlay = self

        def _tick(_mobject: Any, dt: float) -> None:
            clock.advance(dt)
            cue = timeline.cue_at(clock.time)
            cue_id = cue.id if cue else None
            if cue_id != overlay._shown_id:
                overlay._shown_id = cue_id
                overlay.show_text(cue.text if cue else " ")
            overlay._follow_viewport(scene)

        mob.add_updater(_tick)
        first = timeline.cue_at(0.0)
        if first:
            self._shown_id = first.id
            self.show_text(first.text)
        return mob
