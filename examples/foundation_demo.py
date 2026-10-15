"""Part 1 demonstration scene: how a variable stores a value.

Render (from the repository root, with the package installed or PYTHONPATH=src):

    manim -ql examples/foundation_demo.py VariableStoresAValue

This scene uses the shared design system. It does not hard-code brand colors.
On-screen captions are driven by examples/subtitle_demo.json. Those timings
are estimates, not a recording.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from quonitron_manim.components.foundation.variable_store import VariableStore
from quonitron_manim.core.base_scene import QuonitronScene
from quonitron_manim.core.manim_compat import manim_available
from quonitron_manim.design.motion import resolve_rate_function
from quonitron_manim.subtitles import load_track

if manim_available():
    from manim import DOWN, FadeIn, FadeOut, ReplacementTransform, UP
else:  # pragma: no cover
    DOWN = UP = None  # type: ignore[assignment]
    FadeIn = FadeOut = ReplacementTransform = object  # type: ignore[misc, assignment]


class VariableStoresAValue(QuonitronScene):
    """Short explainer demonstrating the Part 1 foundation."""

    render_profile_name = "preview"

    def construct(self) -> None:
        track = load_track(ROOT / "examples" / "subtitle_demo.json")
        easing = resolve_rate_function(self.theme.motion.easing_entrance)
        fast = self.theme.duration("fast")
        normal = self.theme.duration("normal")
        slow = self.theme.duration("slow")
        hold = self.theme.duration("hold")

        title = self.make_title(
            "How a Variable Stores a Value",
            kicker="FOUNDATION",
        )
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=slow, rate_func=easing)
        self.wait(hold)

        self.play(FadeOut(title), run_time=fast)
        heading = self.make_heading("A name that holds a value")
        heading.to_edge(UP, buff=self.theme.spacing.safe_margin)
        overflow = heading.get_top()[1] - self.safe.top
        if overflow > 0:
            heading.shift(DOWN * overflow)
        self.play_write(heading, speed="normal")

        store = VariableStore(
            theme=self.theme,
            variable_name="score",
            value="0",
        )
        box = store.get()
        box.next_to(heading, DOWN, buff=self.theme.spacing.title_to_content)

        caption = self.show_subtitle_text(track.cues[0].text)
        self.play(
            FadeIn(box, shift=DOWN * 0.15),
            FadeIn(caption),
            run_time=normal,
            rate_func=easing,
        )
        self.wait(max(0.2, track.cues[0].duration - normal))

        def swap_caption(index: int, extra=None) -> None:
            nonlocal caption
            nxt = self.show_subtitle_text(track.cues[index].text)
            anims = [FadeOut(caption), FadeIn(nxt)]
            if extra is not None:
                anims.append(extra)
            self.play(*anims, run_time=fast)
            caption = nxt

        swap_caption(1)
        self.wait(max(0.2, track.cues[1].duration - fast))

        swap_caption(2)
        self.wait(max(0.2, track.cues[2].duration - fast))

        new_value = store.make_value("10")
        new_value.move_to(box.value_label.get_center())
        swap_caption(3, ReplacementTransform(box.value_label, new_value))
        box.value_label = new_value
        self.wait(max(0.2, track.cues[3].duration - fast))

        swap_caption(4)
        self.wait(max(0.35, track.cues[4].duration - fast))

        ending = self.make_label("The name stays. The value can change.")
        ending.next_to(box, DOWN, buff=self.theme.spacing.lg)
        self.play(FadeOut(caption), FadeIn(ending), run_time=normal)
        self.wait(hold)
        self.play(
            FadeOut(heading),
            FadeOut(box),
            FadeOut(ending),
            run_time=fast,
        )
