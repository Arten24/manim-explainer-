"""Part 3 demonstration: reusable transitions on the shared timeline.

A variable travels from a simple card, to a source line, to a memory table.
Captions keep the same clock across those conceptual beats.

    manim -ql examples/journey_demo.py CodeToMemoryJourney

Camera zoom uses QuonitronMovingCameraScene. If camera.frame is missing,
the binders fall back to Indicate so the rest of the scene still plays.
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
from quonitron_manim.core.base_scene import QuonitronMovingCameraScene
from quonitron_manim.motion.appearance import FadeInMotion, WriteMotion
from quonitron_manim.motion.emphasis import CircumscribeMotion, IndicateMotion
from quonitron_manim.timeline.models import load_timeline
from quonitron_manim.timeline.player import play_on_scene
from quonitron_manim.transitions.camera import (
    CloseUpToFullTransition,
    ZoomInTransition,
    camera_available,
)
from quonitron_manim.transitions.story import (
    ClosingPreview,
    CodeToMemory,
    ExampleToCode,
    ExplanationToRecap,
    TitleToExplanation,
)


def _memory_row(theme, *, address: str, name: str, value: str):
    from manim import DOWN, RIGHT, RoundedRectangle, VGroup
    from quonitron_manim.core.text import themed_text

    cells = []
    labels = []
    widths = (2.4, 2.2, 2.2)
    texts = (address, name, value)
    roles = ("text_secondary", "accent", "highlight")
    for width, text, role in zip(widths, texts, roles):
        cell = RoundedRectangle(
            width=width,
            height=1.15,
            corner_radius=theme.stroke.corner_radius,
            color=theme.color("border"),
            stroke_width=theme.stroke.regular,
            fill_color=theme.color("surface"),
            fill_opacity=1.0,
        )
        label = themed_text(text, "label", theme, color_role=role)
        label.move_to(cell.get_center())
        group = VGroup(cell, label)
        cells.append(group)
        labels.append(label)
    row = VGroup(*cells).arrange(RIGHT, buff=theme.spacing.sm)
    headers = VGroup(
        *[themed_text(h, "caption", theme, color_role="text_muted") for h in ("address", "name", "value")]
    )
    for header, cell in zip(headers, cells):
        header.next_to(cell, DOWN, buff=theme.spacing.xs)
    table = VGroup(row, headers)
    table.value_cell = cells[2]  # type: ignore[attr-defined]
    table.name_cell = cells[1]  # type: ignore[attr-defined]
    return table


class CodeToMemoryJourney(QuonitronMovingCameraScene):
    """From a variable card, through source code, into a memory diagram."""

    render_profile_name = "preview"

    def construct(self) -> None:
        from manim import DOWN, UP

        timeline = load_timeline(ROOT / "examples" / "journey_timeline.json")
        overlay = SubtitleOverlay(theme=self.theme)

        title = self.make_title(
            "From Code to Memory",
            kicker="TRANSITIONS",
        )
        heading = self.make_heading("A named place in memory")
        heading.to_edge(UP, buff=self.theme.spacing.safe_margin)

        store = VariableStore(theme=self.theme, variable_name="score", value="10")
        card = store.get()
        card.next_to(heading, DOWN, buff=self.theme.spacing.title_to_content)

        code = self.make_body("score = 10")
        code.move_to(card.get_center())

        table = _memory_row(self.theme, address="0x7ffe", name="score", value="10")
        table.move_to(card.get_center())

        recap = self.make_label("A stable name. A replaceable slot.")
        recap.next_to(card, DOWN, buff=self.theme.spacing.lg)

        preview = self.make_caption("Next: how assignment overwrites a slot.")
        preview.next_to(recap, DOWN, buff=self.theme.spacing.sm)

        from quonitron_manim.design.layout import place_in
        self.place_title(heading)
        place_in(card, self.layout_regions["content"])
        code.move_to(card)
        table.move_to(card)
        recap.move_to(card)
        preview.move_to(card)
        for key, mob in dict(title=title, heading=heading, card=card, code=code,
                             table=table, recap=recap, preview=preview).items():
            self.register_layout(key, mob)

        if camera_available(self):
            self.camera.frame.save_state()

        def rt(event):
            return event.animation_duration()

        binders = {
            "ev-title-in": lambda e: FadeInMotion(
                theme=self.theme, run_time=rt(e)
            ).animate(title),
            "ev-title-to-model": lambda e: TitleToExplanation(
                theme=self.theme, run_time=rt(e)
            ).animate(title, card),
            "ev-write-heading": lambda e: WriteMotion(
                theme=self.theme, run_time=rt(e)
            ).animate(heading),
            "ev-mark-card": lambda e: CircumscribeMotion(
                theme=self.theme, run_time=rt(e)
            ).animate(card),
            "ev-example-to-code": lambda e: ExampleToCode(
                theme=self.theme, run_time=rt(e)
            ).animate(card, code),
            "ev-code-to-memory": lambda e: CodeToMemory(
                theme=self.theme, run_time=rt(e)
            ).animate(code, table),
            "ev-zoom-value": lambda e: (
                ZoomInTransition(theme=self.theme, run_time=rt(e), margin=2.2).animate(
                    table.value_cell, scene=self
                )
                if camera_available(self)
                else IndicateMotion(theme=self.theme, run_time=rt(e)).animate(
                    table.value_cell
                )
            ),
            "ev-zoom-full": lambda e: (
                CloseUpToFullTransition(theme=self.theme, run_time=rt(e)).animate(
                    scene=self
                )
                if camera_available(self)
                else IndicateMotion(theme=self.theme, run_time=rt(e)).animate(table)
            ),
            "ev-to-recap": lambda e: ExplanationToRecap(
                theme=self.theme, run_time=rt(e)
            ).animate(table, recap),
            "ev-closing": lambda e: ClosingPreview(
                theme=self.theme, run_time=rt(e)
            ).animate(recap, preview),
        }

        play_on_scene(self, timeline, binders, overlay=overlay)
