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
from quonitron_manim.design.layout import content_area
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

        heading = SceneHeading(theme=self.theme, text="An assignment statement").get()

        sub = Subheading(theme=self.theme, text="Python, read as English").get()

        code = CodeLine(theme=self.theme, text="score = 10").get()

        name_line = HighlightedPhrase(
            theme=self.theme,
            text="score is the name.",
            phrase="score",
        ).get()

        value_line = HighlightedPhrase(
            theme=self.theme,
            text="10 is the value in that slot.",
            phrase="10",
        ).get()

        note = AnnotationCallout(
            theme=self.theme,
            text="The name does not change when the number does.",
        ).get()

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

        recap = BulletList(
            theme=self.theme,
            items=[
                "A name identifies a slot.",
                "A value occupies that slot.",
                "Assignment overwrites the value.",
            ],
        ).get()

        body = BodyParagraph(
            theme=self.theme,
            text="Keep the caption band free: this paragraph sits in the content area, not on top of the subtitles.",
        ).get()

        # Measure complete co-visible beats, not components at their build origin.
        from quonitron_manim.design.layout import SafeArea, stack_in, place_in, LayoutItem
        header = [title, heading, sub]
        stack_in(header, box, gap=self.theme.spacing.xs)
        lesson = SafeArea(box.left, box.right, box.bottom,
                          sub.get_bottom()[1] - self.theme.spacing.md)
        stack_in([code, name_line, value_line, note], lesson, gap=self.theme.spacing.xs)
        equation.next_to(code, DOWN, buff=self.theme.spacing.xs)
        counter.next_to(equation, DOWN, buff=self.theme.spacing.xs)
        eleven.move_to(counter)
        for mob in (steps, recap, body):
            place_in(mob, lesson)
        objects = dict(title=title, heading=heading, sub=sub, code=code,
                       name=name_line, value=value_line, note=note, equation=equation,
                       counter=counter, eleven=eleven, steps=steps, recap=recap, body=body)
        for key, mob in objects.items():
            self.register_layout(key, mob)
        # Layout preflight is phase-aware: replacements are not simultaneous objects.
        for phase in (["code", "name", "value", "note"], ["code", "equation", "counter"],
                      ["steps"], ["recap"], ["body"]):
            issues = self.layout_validator.validate(
                [LayoutItem(key, objects[key]) for key in ["title", "heading", "sub"] + phase])
            if any(i.severity == "ERROR" for i in issues):
                raise ValueError("\n".join(map(str, issues)))

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
            "ev-recap": lambda e: self.readable_swap(steps, recap, run_time=rt(e)),
            "ev-body": lambda e: self.readable_swap(recap, body, run_time=rt(e)),
        }

        play_on_scene(self, timeline, binders, overlay=overlay)
