"""On-screen subtitle overlay driven by the shared timeline.

Styling comes from the theme. Timing comes only from Timeline.cue_at().
"""

from __future__ import annotations

from typing import Any, Optional

from quonitron_manim.core.component import Component, register_component
from quonitron_manim.design.layout import safe_area, subtitle_anchor
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

    def build(self) -> Any:
        from quonitron_manim.core.text import subtitle_text

        self._canonical = subtitle_text(self.param("text", " "), self.theme)
        self._mob = self._canonical.copy()
        return self._mob

    def _restyle(self, text: str) -> None:
        from quonitron_manim.core.text import subtitle_text

        self._canonical = subtitle_text(text, self.theme)
        self._mob.become(self._canonical)

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
            # MovingCamera has no fixed-in-frame API: project canonical geometry
            # into its viewport, including at intermediate animation frames.
            frame = getattr(getattr(scene, "camera", None), "frame", None)
            if frame is not None:
                projected = overlay._canonical.copy()
                projected.scale(frame.width / overlay.theme.frame_width, about_point=[0, 0, 0])
                projected.shift(frame.get_center())
                mob.become(projected)

        mob.add_updater(_tick)
        first = timeline.cue_at(0.0)
        if first:
            self._shown_id = first.id
            self.show_text(first.text)
        return mob
