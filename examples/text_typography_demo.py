"""Part 4 demonstration: typography components on the shared timeline.

    manim -ql examples/text_typography_demo.py AssignmentInType

Captions, SRT/VTT, and animation durations all read
``examples/text_timeline.json``. Timings are estimates, not a recording.
Educational copy stays in the content area above the subtitle band.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from quonitron_manim.components.foundation.subtitle_overlay import SubtitleOverlay
from quonitron_manim.components.text import (
    AnnotationCallout,
    BodyParagraph,
    BulletList,
    CodeLine,
    CounterLabel,
    DisplayTitle,
    EquationText,
    HighlightedPhrase,
    SceneHeading,
    StepList,
    Subheading,
)
from quonitron_manim.core.base_scene import QuonitronScene
from quonitron_manim.design.layout import content_area, title_anchor
from quonitron_manim.motion.appearance import FadeInMotion, FadeOutMotion, WriteMotion
from quonitron_manim.motion.emphasis import IndicateMotion
from quonitron_manim.motion.transform import ReplacementTransformMotion
from quonitron_manim.timeline.models import load_timeline
from quonitron_manim.timeline.player import play_on_scene


class AssignmentInType(QuonitronScene):
    """How an assignment statement names a value — told with type, not gadgets."""

    render_profile_name = "preview"

    def construct(self) -> None:
        from manim import DOWN

        timeline = load_timeline(ROOT / "examples" / "text_timeline.json")
        overlay = SubtitleOverlay(theme=self.theme)
        box = content_area(
            self.theme.frame_width,
            self.theme.frame_height,
            self.theme.spacing.safe_margin,
        )

        title = DisplayTitle(theme=self.theme, text="A Name for a Value").get()
        title.move_to(title_anchor(self.safe, lift=self.theme.spacing.sm))

        heading = SceneHeading(theme=self.theme, text="An assignment statement").get()
        heading.next_to(title, DOWN, buff=self.theme.spacing.md)
        if heading.get_left()[0] < box.left:
            heading.shift([box.left - heading.get_left()[0], 0, 0])

        sub = Subheading(theme=self.theme, text="Python, read as English").get()
        sub.next_to(heading, DOWN, buff=self.theme.spacing.sm)

        code = CodeLine(theme=self.theme, text="score = 10").get()
        code.move_to([0, 0.35, 0])

        name_line = HighlightedPhrase(
            theme=self.theme,
            text="score is the name.",
            phrase="score",
        ).get()
        name_line.next_to(code, DOWN, buff=self.theme.spacing.md)

        value_line = HighlightedPhrase(
            theme=self.theme,
            text="10 is the value in that slot.",
            phrase="10",
        ).get()
        value_line.next_to(name_line, DOWN, buff=self.theme.spacing.sm)

        note = AnnotationCallout(
            theme=self.theme,
            text="The name does not change when the number does.",
        ).get()
        note.next_to(value_line, DOWN, buff=self.theme.spacing.md)

        equation = EquationText(theme=self.theme, tex="score = 10").get()
        equation.next_to(code, DOWN, buff=self.theme.spacing.lg)

        counter = CounterLabel(theme=self.theme, value="10", label="stored value").get()
        counter.next_to(equation, DOWN, buff=self.theme.spacing.md)
        eleven = CounterLabel(theme=self.theme, value="11", label="stored value").get()
        eleven.move_to(counter.get_center())

        steps = StepList(
            theme=self.theme,
            items=[
                "Choose a name.",
                "Write an assignment.",
                "Replace only the value.",
            ],
        ).get()
        steps.move_to([0, 0.55, 0])

        recap = BulletList(
            theme=self.theme,
            items=[
                "A name identifies a slot.",
                "A value occupies that slot.",
                "Assignment overwrites the value.",
            ],
        ).get()
        recap.move_to([0, -0.2, 0])

        body = BodyParagraph(
            theme=self.theme,
            text="Keep the caption band free: this paragraph sits in the content area, not on top of the subtitles.",
        ).get()
        body.next_to(recap, DOWN, buff=self.theme.spacing.sm)

        def rt(event):
            return event.animation_duration()

        from manim import AnimationGroup

        binders = {
            "ev-title": lambda e: FadeInMotion(theme=self.theme, run_time=rt(e)).animate(title),
            "ev-heading": lambda e: WriteMotion(theme=self.theme, run_time=rt(e)).animate(heading),
            "ev-sub": lambda e: FadeInMotion(theme=self.theme, run_time=rt(e)).animate(sub),
            "ev-code": lambda e: WriteMotion(theme=self.theme, run_time=rt(e)).animate(code),
            "ev-name": lambda e: FadeInMotion(theme=self.theme, run_time=rt(e)).animate(name_line),
            "ev-indicate-name": lambda e: IndicateMotion(
                theme=self.theme, run_time=rt(e)
            ).animate(name_line.phrase),
            "ev-value": lambda e: FadeInMotion(theme=self.theme, run_time=rt(e)).animate(value_line),
            "ev-indicate-value": lambda e: IndicateMotion(
                theme=self.theme, run_time=rt(e)
            ).animate(value_line.phrase),
            "ev-note": lambda e: FadeInMotion(theme=self.theme, run_time=rt(e)).animate(note),
            "ev-clear-explain": lambda e: AnimationGroup(
                FadeOutMotion(theme=self.theme, run_time=rt(e)).animate(name_line),
                FadeOutMotion(theme=self.theme, run_time=rt(e)).animate(value_line),
                FadeOutMotion(theme=self.theme, run_time=rt(e)).animate(note),
            ),
            "ev-equation": lambda e: FadeInMotion(theme=self.theme, run_time=rt(e)).animate(equation),
            "ev-counter": lambda e: FadeInMotion(theme=self.theme, run_time=rt(e)).animate(counter),
            "ev-replace": lambda e: ReplacementTransformMotion(
                theme=self.theme, run_time=rt(e)
            ).animate(counter, eleven),
            "ev-clear-code": lambda e: AnimationGroup(
                FadeOutMotion(theme=self.theme, run_time=rt(e)).animate(code),
                FadeOutMotion(theme=self.theme, run_time=rt(e)).animate(equation),
                FadeOutMotion(theme=self.theme, run_time=rt(e)).animate(eleven),
            ),
            "ev-steps": lambda e: FadeInMotion(theme=self.theme, run_time=rt(e)).animate(steps),
            "ev-recap": lambda e: FadeInMotion(theme=self.theme, run_time=rt(e)).animate(recap),
            "ev-body": lambda e: FadeInMotion(theme=self.theme, run_time=rt(e)).animate(body),
        }

        play_on_scene(self, timeline, binders, overlay=overlay)
