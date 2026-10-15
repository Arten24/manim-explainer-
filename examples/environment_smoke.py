"""Environment-only smoke scenes. No new library feature or development Part.

    python -m manim -ql examples/environment_smoke.py MinimalRenderCheck
    python -m manim -ql examples/environment_smoke.py ThemeSubtitleRenderCheck
"""
from manim import Circle, Create, FadeIn, Scene, Text, VGroup

from quonitron_manim.core.base_scene import QuonitronScene
from quonitron_manim.design.layout import LayoutItem, stack_in


class MinimalRenderCheck(Scene):
    """Exercise Cairo paths, Pango Text and PyAV movie output without LaTeX."""
    def construct(self):
        shape = Circle(radius=0.7).shift([0, -0.7, 0])
        label = Text('Manim rendering works', font_size=32).shift([0, 1.0, 0])
        self.play(Create(shape), FadeIn(label), run_time=0.8)
        self.wait(0.8)


class ThemeSubtitleRenderCheck(QuonitronScene):
    """Existing theme, subtitle helper and measured collision-free placement."""
    def construct(self):
        title = self.make_heading('QUONITRON render verification')
        body = self.make_body('The lesson stays above the reserved subtitle band.')
        circle = Circle(radius=0.5, color=self.theme.color('accent'))
        content = [title, body, circle]
        stack_in(content, self.layout_regions['content'], gap=self.theme.spacing.md)
        caption = self.show_subtitle_text('A readable caption sits in its own safe region.')
        for object_id, mob in zip(('title', 'body', 'circle'), content):
            self.register_layout(object_id, mob)
        issues = self.layout_validator.validate(
            [LayoutItem(name, mob) for name, mob in zip(('title', 'body', 'circle'), content)]
            + [LayoutItem('caption', caption, 'subtitle')])
        if any(issue.severity == 'ERROR' for issue in issues):
            raise RuntimeError('\n'.join(map(str, issues)))
        self.play(FadeIn(VGroup(*content)), FadeIn(caption), run_time=0.8)
        self.wait(1.2)
