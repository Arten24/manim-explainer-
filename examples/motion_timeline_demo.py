"""Part 2 demonstration: shared motion library + subtitle timeline.

Render from the repository root:

    manim -ql examples/motion_timeline_demo.py VariableMemoryTimeline

On-screen captions, SRT/VTT, and animation run_times all read
``examples/variable_timeline.json``. Timings are estimated, not a recording.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from quonitron_manim.components.foundation.subtitle_overlay import SubtitleOverlay
from quonitron_manim.components.foundation.variable_store import VariableStore
from quonitron_manim.core.base_scene import QuonitronScene
from quonitron_manim.motion.appearance import (
    FadeInMotion,
    GrowFromCenterMotion,
    SmoothEntranceMotion,
    SmoothExitMotion,
    WriteMotion,
)
from quonitron_manim.motion.emphasis import (
    CircumscribeMotion,
    FocusSetMotion,
    IndicateMotion,
    PulseMotion,
)
from quonitron_manim.motion.math_utils import CreateLineMotion
from quonitron_manim.motion.transform import ReplacementTransformMotion
from quonitron_manim.timeline.models import load_timeline
from quonitron_manim.timeline.player import play_on_scene


class VariableMemoryTimeline(QuonitronScene):
    """How a variable stores a value — driven by one shared timeline."""

    render_profile_name = "preview"

    def construct(self) -> None:
        from manim import DOWN, UP, AnimationGroup, FadeOut, Line

        timeline = load_timeline(ROOT / "examples" / "variable_timeline.json")
        overlay = SubtitleOverlay(theme=self.theme)

        title = self.make_title(
            "How a Variable Stores a Value",
            kicker="MOTION + TIMELINE",
        )
        heading = self.make_heading("A named place in memory")
        heading.to_edge(UP, buff=self.theme.spacing.safe_margin)
        overflow = heading.get_top()[1] - self.safe.top
        if overflow > 0:
            heading.shift(DOWN * overflow)

        store = VariableStore(theme=self.theme, variable_name="score", value="0")
        box = store.get()
        box.next_to(heading, DOWN, buff=self.theme.spacing.title_to_content)

        recap = self.make_label("A stable name. A replaceable value.")
        recap.next_to(box, DOWN, buff=self.theme.spacing.lg)

        arrow = Line(
            box.name_label.get_bottom() + DOWN * 0.08,
            box.value_label.get_top() + UP * 0.08,
            color=self.theme.color("accent"),
            stroke_width=self.theme.stroke.thin,
        )

        from quonitron_manim.design.layout import stack_in
        stack_in([heading, box, recap], self.layout_regions["content"],
                 gap=self.theme.spacing.md)
        # The connector is constructed before reflow; recompute its endpoints.
        arrow.put_start_and_end_on(box.name_label.get_bottom() + DOWN * 0.08,
                                  box.value_label.get_top() + UP * 0.08)
        for key, mob in dict(title=title, heading=heading, card=box.card,
                             name=box.name_label, value=box.value_label, recap=recap).items():
            self.register_layout(key, mob)
        for key in ("name", "value"):
            self.layout_validator.allow("card", key, reason="label contained in variable card")

        def duration(event):
            return {"run_time": event.animation_duration()}

        def replace_value(event):
            new_value = store.make_value("10")
            new_value.move_to(box.value_label.get_center())
            anim = ReplacementTransformMotion(theme=self.theme, **duration(event)).animate(
                box.value_label, new_value
            )
            box.value_label = new_value
            from quonitron_manim.design.layout import LayoutItem
            self.layout_items["value"] = LayoutItem("value", new_value)
            return anim

        def fade_end(event):
            leftovers = [heading, box, recap, arrow]
            return AnimationGroup(
                *[FadeOut(mob) for mob in leftovers],
                run_time=event.animation_duration(),
            )

        binders = {
            "ev_title_in": lambda e: SmoothEntranceMotion(
                theme=self.theme, **duration(e)
            ).animate(title),
            "ev_title_out": lambda e: SmoothExitMotion(
                theme=self.theme, **duration(e)
            ).animate(title),
            "ev_heading": lambda e: WriteMotion(theme=self.theme, **duration(e)).animate(
                heading
            ),
            "ev_box": lambda e: GrowFromCenterMotion(
                theme=self.theme, **duration(e)
            ).animate(box.card),
            "ev_name": lambda e: WriteMotion(theme=self.theme, **duration(e)).animate(
                box.name_label
            ),
            "ev_value0": lambda e: FadeInMotion(theme=self.theme, **duration(e)).animate(
                box.value_label
            ),
            "ev_indicate": lambda e: IndicateMotion(
                theme=self.theme, **duration(e)
            ).animate(box.card),
            "ev_circ_name": lambda e: CircumscribeMotion(
                theme=self.theme, **duration(e)
            ).animate(box.name_label),
            "ev_arrow": lambda e: CreateLineMotion(
                theme=self.theme, **duration(e)
            ).animate(arrow),
            "ev_replace": replace_value,
            "ev_pulse": lambda e: PulseMotion(theme=self.theme, **duration(e)).animate(
                box.value_label
            ),
            "ev_focus": lambda e: FocusSetMotion(theme=self.theme, **duration(e)).animate(
                box.card, heading, recap
            ),
            "ev_recap": lambda e: SmoothEntranceMotion(
                theme=self.theme, **duration(e)
            ).animate(recap),
            "ev_end": fade_end,
        }

        play_on_scene(self, timeline, binders, overlay=overlay)
