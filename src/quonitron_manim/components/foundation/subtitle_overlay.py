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
        from quonitron_manim.core.text import themed_text

        text = self.param("text", " ")
        mob = themed_text(text, "caption", self.theme)
        area = safe_area(
            self.theme.frame_width,
            self.theme.frame_height,
            self.theme.spacing.safe_margin,
        )
        x, y, z = subtitle_anchor(area, drop=self.theme.spacing.xs)
        max_width = area.width * 0.96
        if mob.width > max_width:
            mob.width = max_width
        mob.move_to([x, y, z])
        overflow = area.bottom - mob.get_bottom()[1]
        if overflow > 0:
            mob.shift([0, overflow, 0])
        self._mob = mob
        return mob

    def _restyle(self, text: str) -> None:
        from quonitron_manim.core.text import themed_text

        replacement = themed_text(text or " ", "caption", self.theme)
        area = safe_area(
            self.theme.frame_width,
            self.theme.frame_height,
            self.theme.spacing.safe_margin,
        )
        max_width = area.width * 0.96
        if replacement.width > max_width:
            replacement.width = max_width
        replacement.move_to(self._mob.get_center())
        self._mob.become(replacement)

    def show_text(self, text: str) -> None:
        if self._mob is None:
            self.get()
        self._restyle(text)

    def attach(self, scene: Any, timeline: Timeline, clock: TimelineClock) -> Any:
        self.timeline = timeline
        self.clock = clock
        mob = self.get()
        scene.add(mob)
        overlay = self

        def _tick(_mobject: Any, dt: float) -> None:
            clock.advance(dt)
            cue = timeline.cue_at(clock.time)
            cue_id = cue.id if cue else None
            if cue_id == overlay._shown_id:
                return
            overlay._shown_id = cue_id
            overlay.show_text(cue.text if cue else " ")

        mob.add_updater(_tick)
        first = timeline.cue_at(0.0)
        if first:
            self._shown_id = first.id
            self.show_text(first.text)
        return mob
