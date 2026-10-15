"""Repair exercise, NOT a new Part. No TeX dependency. Render with -ql."""
from quonitron_manim.core.base_scene import QuonitronScene


class LayoutRepairExercise(QuonitronScene):
    def construct(self):
        from manim import Arrow, FadeIn, RoundedRectangle, VGroup
        from quonitron_manim.core.text import measured_text, themed_text
        from quonitron_manim.design.layout import (
            LayoutItem, LayoutValidator, SafeArea, place_in, place_label, stack_in,
        )
        area = self.layout_regions["content"]
        heading = self.make_heading("Layout repair: readable by construction")
        paragraph = measured_text(
            "A name identifies a memory slot. When a new value is assigned, the name "
            "continues to identify the same slot. This longer explanation wraps using "
            "the actual font geometry, rather than shrinking the text to fit.",
            theme=self.theme, max_width=area.width, max_height=3)
        stack_in([heading, paragraph], area, gap=self.theme.spacing.md)
        caption = self.show_subtitle_text("Captions have a reserved bottom band, at a fixed readable size.")
        self.register_layout("heading", heading)
        self.register_layout("paragraph", paragraph)
        self.play(FadeIn(heading), FadeIn(paragraph), FadeIn(caption))
        self.wait(2)
        panel = RoundedRectangle(width=3.5, height=1.5)
        value = themed_text("10", "title", self.theme)
        value.move_to(panel)
        label = themed_text("score", "label", self.theme)
        diagram_area = SafeArea(area.left, area.right, area.bottom,
                                heading.get_bottom()[1] - self.theme.spacing.md)
        place_in(panel, diagram_area)
        value.move_to(panel)
        place_label(label, panel, diagram_area, gap=0.6)
        arrow = Arrow(label.get_left(), panel.get_right(), buff=0.12)
        diagram = VGroup(panel, value, label, arrow)
        self.register_layout("diagram", diagram)
        self.play(self.readable_swap(paragraph, diagram, run_time=1.2))
        self.wait(2)
        # Deliberately conflicting pair: report it without obscuring the real lesson.
        validator = LayoutValidator(self.layout_regions, scene=type(self).__name__)
        for issue in validator.validate([LayoutItem("label-a", label),
                                         LayoutItem("label-b", label.copy())]):
            print(issue)
