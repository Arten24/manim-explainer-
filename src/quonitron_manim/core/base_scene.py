"""Base scene that applies the QUONITRON theme.

Do not override ``__init__`` on Manim scenes. Put setup work in ``setup``.
"""

from __future__ import annotations

from typing import Any, Optional

from quonitron_manim.config import get_render_profile
from quonitron_manim.core.manim_compat import manim_available
from quonitron_manim.design.layout import (safe_area, subtitle_anchor, title_anchor,
    layout_regions, LayoutValidator, LayoutItem)
from quonitron_manim.design.motion import resolve_rate_function
from quonitron_manim.design.theme import Theme, apply_theme_to_manim, get_theme

try:
    from manim import DOWN, FadeIn, FadeOut, Scene, Write
except Exception:  # pragma: no cover
    class Scene:  # type: ignore[no-redef]
        def setup(self) -> None:
            return None

        def construct(self) -> None:
            return None

        def play(self, *args: Any, **kwargs: Any) -> None:
            return None

        def add(self, *args: Any, **kwargs: Any) -> None:
            return None

        def wait(self, *args: Any, **kwargs: Any) -> None:
            return None

        def remove(self, *args: Any, **kwargs: Any) -> None:
            return None

    DOWN = None  # type: ignore[assignment]
    FadeIn = FadeOut = Write = object  # type: ignore[misc, assignment]

try:
    from manim import MovingCameraScene as _MovingCameraScene
except Exception:  # pragma: no cover
    _MovingCameraScene = Scene  # type: ignore[misc, assignment]


class QuonitronSceneMixin:
    """Shared helpers for titles, headings, captions, and timing."""

    theme_name: str = "quonitron_dark"
    render_profile_name: Optional[str] = None

    def setup(self) -> None:
        parent_setup = getattr(super(), "setup", None)
        if callable(parent_setup):
            parent_setup()
        self.theme: Theme = get_theme(self.theme_name)
        apply_theme_to_manim(self.theme)
        profile_name = self.render_profile_name or self.theme.render_profile
        self.render_profile = get_render_profile(profile_name)
        self.layout_regions = layout_regions(self.theme.frame_width, self.theme.frame_height,
                                             self.theme.spacing.safe_margin)
        self.layout_validator = LayoutValidator(self.layout_regions, scene=type(self).__name__)
        self.layout_items = {}
        self._layout_reported = set()
        self.safe = safe_area(
            self.theme.frame_width,
            self.theme.frame_height,
            self.theme.spacing.safe_margin,
        )
        if manim_available() and hasattr(self, "camera"):
            self.camera.background_color = self.theme.color("background")

    def make_title(self, text: str, **kwargs: Any):
        from quonitron_manim.components.foundation.title_card import TitleCard

        return TitleCard(theme=self.theme, title=text, **kwargs).get()

    def make_heading(self, text: str, **kwargs: Any):
        from quonitron_manim.components.foundation.section_heading import (
            SectionHeading,
        )

        return SectionHeading(theme=self.theme, text=text, **kwargs).get()

    def _make_wrapped(self, text, role, **kwargs):
        from quonitron_manim.core.text import measured_text
        area = self.layout_regions["content"]
        max_width = kwargs.pop("max_width", area.width)
        return measured_text(text, role, self.theme, max_width=min(max_width, area.width),
                             max_height=area.height, **kwargs)

    def make_body(self, text: str, **kwargs: Any):
        return self._make_wrapped(text, "body", **kwargs)

    def make_label(self, text: str, **kwargs: Any):
        return self._make_wrapped(text, "label", **kwargs)

    def make_caption(self, text: str, **kwargs: Any):
        return self._make_wrapped(text, "caption", **kwargs)

    def place_title(self, mobject: Any) -> Any:
        x, y, z = title_anchor(self.safe, lift=self.theme.spacing.sm)
        mobject.move_to([x, y, z])
        overflow = mobject.get_top()[1] - self.safe.top
        if overflow > 0:
            mobject.shift([0, -overflow, 0])
        return mobject

    def place_caption(self, mobject: Any) -> Any:
        x, y, z = subtitle_anchor(self.safe, drop=self.theme.spacing.xs)
        mobject.move_to([x, y, z])
        overflow = self.safe.bottom - mobject.get_bottom()[1]
        if overflow > 0:
            mobject.shift([0, overflow, 0])
        return mobject

    def play_entrance(self, *mobjects: Any, speed: str = "normal", **kwargs: Any):
        run_time = kwargs.pop("run_time", self.theme.duration(speed))
        rate_func = kwargs.pop(
            "rate_func",
            resolve_rate_function(self.theme.motion.easing_entrance),
        )
        anims = [FadeIn(mob, shift=DOWN * 0.15, **kwargs) for mob in mobjects]
        self.play(*anims, run_time=run_time, rate_func=rate_func)

    def play_write(self, mobject: Any, speed: str = "slow", **kwargs: Any):
        run_time = kwargs.pop("run_time", self.theme.duration(speed))
        rate_func = kwargs.pop(
            "rate_func",
            resolve_rate_function(self.theme.motion.easing_default),
        )
        self.play(Write(mobject), run_time=run_time, rate_func=rate_func, **kwargs)

    def fade_out(self, *mobjects: Any, speed: str = "fast", **kwargs: Any):
        run_time = kwargs.pop("run_time", self.theme.duration(speed))
        self.play(*[FadeOut(mob) for mob in mobjects], run_time=run_time, **kwargs)

    def hold(self, speed: str = "hold") -> None:
        self.wait(self.theme.duration(speed))

    def show_subtitle_text(self, text: str, **kwargs: Any):
        """On-screen caption. Independent of SRT/VTT export files."""
        from quonitron_manim.core.text import subtitle_text
        caption = subtitle_text(text, self.theme, **kwargs)
        self.register_layout(f"subtitle-{len(self.layout_items)}", caption, region="subtitle")
        return caption

    def readable_swap(self, outgoing, incoming, *, run_time=1.0):
        """Non-overlapping editorial swap for unrelated text in the same region."""
        from manim import Succession, FadeOut, FadeIn
        return Succession(FadeOut(outgoing, run_time=run_time / 2),
                          FadeIn(incoming, run_time=run_time / 2))

    def register_layout(self, object_id, mobject, *, region="content"):
        """Register semantic objects, not glyphs. IDs must be unique per scene."""
        if object_id in self.layout_items:
            raise ValueError(f"Duplicate layout ID: {object_id}")
        self.layout_items[object_id] = LayoutItem(object_id, mobject, region)
        return mobject

    def check_layout(self, *, visible_only=True):
        import warnings
        items = list(self.layout_items.values())
        if visible_only:
            family = {id(m) for root in getattr(self, "mobjects", []) for m in root.get_family()}
            items = [i for i in items if id(i.mobject) in family]
        frame = getattr(getattr(self, "camera", None), "frame", None)
        if frame is not None:
            projected = []
            for item in items:
                mob = item.mobject.copy()
                mob.shift(-frame.get_center())
                mob.scale(self.theme.frame_width / frame.width, about_point=[0, 0, 0])
                projected.append(LayoutItem(item.id, mob, item.region))
            items = projected
        issues = self.layout_validator.validate(items)
        for issue in issues:
            key = (issue.severity, issue.ids, issue.message)
            if issue.severity != "INFO" and key not in self._layout_reported:
                warnings.warn(str(issue), UserWarning, stacklevel=2)
                self._layout_reported.add(key)
        return issues

    def play(self, *args, **kwargs):
        result = super().play(*args, **kwargs)
        if hasattr(self, "layout_items"):
            self.check_layout()
        return result



class QuonitronScene(QuonitronSceneMixin, Scene):
    """Default Cairo scene. Use QuonitronMovingCameraScene for pan/zoom."""


class QuonitronMovingCameraScene(QuonitronSceneMixin, _MovingCameraScene):
    """Scene with manim.MovingCamera (camera.frame). Required for camera transitions."""
