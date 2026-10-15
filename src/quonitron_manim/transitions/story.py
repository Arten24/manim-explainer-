"""Educational storytelling templates. Compositions, not one-off videos."""

from __future__ import annotations

from typing import Any

from quonitron_manim.motion.appearance import FadeInMotion, FadeOutMotion, WriteMotion
from quonitron_manim.motion.base import MotionError, import_manim
from quonitron_manim.transitions.base import TransitionRecipe, transition_component
from quonitron_manim.transitions.continuity import MorphTransition
from quonitron_manim.transitions.simple import FadeTransition, SlideTransition


def _pair(targets):
    if len(targets) < 2:
        raise MotionError("story templates need the outgoing layout and the incoming layout")
    return targets[0], targets[1]


@transition_component
class TitleToExplanation(TransitionRecipe):
    """Title card yields to the first explanatory visual."""

    component_id = "transition.story.title_to_explanation"
    name = "Title To Explanation"
    subcategory = "story"
    manim_api = "Succession"
    tags = ["title", "story", "opening"]
    aliases = ["title to explanation"]
    use_cases = ["Open an explainer without a hard cut"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        title, explanation = _pair(targets)
        rt = self.run_time()
        return manim.Succession(
            FadeOutMotion(theme=self.theme, run_time=rt * 0.4).animate(title),
            WriteMotion(theme=self.theme, run_time=rt * 0.6).animate(explanation),
        )


@transition_component
class ExplanationToExample(TransitionRecipe):
    """Slide from a definition into a worked example."""

    component_id = "transition.story.explanation_to_example"
    name = "Explanation To Example"
    subcategory = "story"
    manim_api = "SlideTransition"
    tags = ["example", "story"]
    aliases = ["explanation to worked example"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        return SlideTransition(
            theme=self.theme, run_time=self.run_time(), direction="LEFT"
        ).animate(*targets)


@transition_component
class ExampleToCode(TransitionRecipe):
    """Morph or replace an example object into a source-code representation."""

    component_id = "transition.story.example_to_code"
    name = "Example To Code"
    subcategory = "story"
    manim_api = "ReplacementTransform"
    tags = ["code", "story", "continuity"]
    aliases = ["example to code"]
    use_cases = ["A variable box becoming the assignment statement that created it"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        return MorphTransition(theme=self.theme, run_time=self.run_time()).animate(*targets)


@transition_component
class CodeToTrace(TransitionRecipe):
    """Slide from a code snippet into an execution-trace layout."""

    component_id = "transition.story.code_to_trace"
    name = "Code To Trace"
    subcategory = "story"
    manim_api = "SlideTransition"
    tags = ["trace", "code", "story"]
    aliases = ["code to execution trace"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        return SlideTransition(
            theme=self.theme, run_time=self.run_time(), direction="UP"
        ).animate(*targets)


@transition_component
class CodeToMemory(TransitionRecipe):
    """Carry the identifier from a code line into a memory-diagram cell."""

    component_id = "transition.story.code_to_memory"
    name = "Code To Memory"
    subcategory = "story"
    manim_api = "FadeTransform"
    tags = ["memory", "code", "architecture", "story"]
    aliases = ["code to memory or architecture diagram"]
    use_cases = ["Show that a name in source is a labeled slot in memory"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        from quonitron_manim.transitions.continuity import SimplifyToDetailTransition

        return SimplifyToDetailTransition(
            theme=self.theme, run_time=self.run_time()
        ).animate(*targets)


@transition_component
class DiagramToChart(TransitionRecipe):
    """Fade-transform a diagram into a chart-shaped layout (chart library is Part 7)."""

    component_id = "transition.story.diagram_to_chart"
    name = "Diagram To Chart"
    subcategory = "story"
    manim_api = "FadeTransform"
    tags = ["chart", "diagram", "story"]
    aliases = ["diagram to chart"]
    limitations = "Does not draw axes. Pass a chart mobject from a later part when it exists."

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        return FadeTransition(theme=self.theme, run_time=self.run_time()).animate(*targets)


@transition_component
class ExplanationToRecap(TransitionRecipe):
    """Settle into a recap line after the detailed explanation."""

    component_id = "transition.story.explanation_to_recap"
    name = "Explanation To Recap"
    subcategory = "story"
    manim_api = "FadeTransition"
    tags = ["recap", "story"]
    aliases = ["detailed explanation to recap"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        return FadeTransition(theme=self.theme, run_time=self.run_time()).animate(*targets)


@transition_component
class ChapterBreak(TransitionRecipe):
    """One chapter to the next: brief fade, not a decorative flourish."""

    component_id = "transition.story.chapter_break"
    name = "Chapter Break"
    subcategory = "story"
    manim_api = "FadeTransition"
    tags = ["chapter", "story"]
    aliases = ["one chapter to the next"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        return FadeTransition(theme=self.theme, run_time=self.run_time()).animate(*targets)


@transition_component
class ClosingPreview(TransitionRecipe):
    """Closing scene plus a quiet next-topic preview."""

    component_id = "transition.story.closing_preview"
    name = "Closing Preview"
    subcategory = "story"
    manim_api = "Succession"
    tags = ["closing", "preview", "story"]
    aliases = ["closing scene and next-topic preview"]

    def animate(self, *targets: Any, **kwargs: Any) -> Any:
        self.validate()
        manim = import_manim()
        current, preview = _pair(targets)
        rt = self.run_time()
        return manim.Succession(
            FadeOutMotion(theme=self.theme, run_time=rt * 0.5).animate(current),
            FadeInMotion(theme=self.theme, run_time=rt * 0.5).animate(preview),
        )
