"""Margins, safe areas, spacing scale, and stroke tokens.

Manim's default frame is 8 units tall. At 16:9 the width is 14.222….
Values here are in those scene units, not pixels.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Spacing:
    """Spacing scale. Use these instead of magic numbers in scenes."""

    xxs: float = 0.08
    xs: float = 0.16
    sm: float = 0.28
    md: float = 0.40
    lg: float = 0.64
    xl: float = 1.00
    margin: float = 0.55
    safe_margin: float = 0.80
    gutter: float = 0.40
    card_padding: float = 0.32
    title_to_content: float = 0.70


@dataclass(frozen=True)
class Stroke:
    hairline: float = 1.0
    thin: float = 1.5
    regular: float = 2.25
    thick: float = 3.5
    corner_radius: float = 0.16


@dataclass(frozen=True)
class SafeArea:
    left: float
    right: float
    bottom: float
    top: float

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.top - self.bottom


def safe_area(
    frame_width: float = 14.222222,
    frame_height: float = 8.0,
    margin: float = 0.80,
) -> SafeArea:
    half_w = frame_width / 2.0
    half_h = frame_height / 2.0
    return SafeArea(
        left=-half_w + margin,
        right=half_w - margin,
        bottom=-half_h + margin,
        top=half_h - margin,
    )


def title_anchor(area: SafeArea, lift: float = 0.15) -> Tuple[float, float, float]:
    """World coordinates for a top-centered title."""
    return (0.0, area.top - lift, 0.0)


def subtitle_anchor(area: SafeArea, drop: float = 0.10) -> Tuple[float, float, float]:
    """World coordinates for a bottom caption / subtitle cue."""
    return (0.0, area.bottom + drop, 0.0)


def content_area(
    frame_width: float = 14.222222,
    frame_height: float = 8.0,
    margin: float = 0.80,
    caption_band: float = 1.05,
) -> SafeArea:
    """Safe area with the bottom caption band reserved for SubtitleOverlay."""
    area = safe_area(frame_width, frame_height, margin)
    band = max(0.0, float(caption_band))
    return SafeArea(
        left=area.left,
        right=area.right,
        bottom=area.bottom + band + (0.16 if band else 0.0),
        top=area.top,
    )


def box_overflow(
    left: float,
    right: float,
    bottom: float,
    top: float,
    area: SafeArea,
    *,
    tol: float = 1e-6,
) -> list:
    """Return side names where a bounding box leaves ``area``."""
    hits = []
    if left < area.left - tol:
        hits.append("left")
    if right > area.right + tol:
        hits.append("right")
    if bottom < area.bottom - tol:
        hits.append("bottom")
    if top > area.top + tol:
        hits.append("top")
    return hits


class LayoutError(ValueError):
    """Content needs reflow, pagination, or a different layout; never shrink silently."""


def bounds(mobject) -> SafeArea:
    """Measure public Manim geometry (also usable with geometry test doubles)."""
    left, right = float(mobject.get_left()[0]), float(mobject.get_right()[0])
    bottom, top = float(mobject.get_bottom()[1]), float(mobject.get_top()[1])
    # Horizontal/vertical connectors have zero-area path bounds, but visible stroke.
    # Use a conservative scene-unit footprint so they cannot disappear from checks.
    if hasattr(mobject, "get_start") and hasattr(mobject, "get_end"):
        if right - left < 0.03:
            left, right = left - 0.015, right + 0.015
        if top - bottom < 0.03:
            bottom, top = bottom - 0.015, top + 0.015
    return SafeArea(left, right, bottom, top)


def layout_regions(frame_width=14.222222, frame_height=8.0, margin=0.80,
                   caption_band=1.05, gutter=0.16):
    safe = safe_area(frame_width, frame_height, margin)
    if caption_band <= 0 or caption_band + gutter >= safe.height:
        raise LayoutError("Subtitle band must leave room for content")
    return {
        "safe": safe,
        "subtitle": SafeArea(safe.left, safe.right, safe.bottom, safe.bottom + caption_band),
        "content": SafeArea(safe.left, safe.right, safe.bottom + caption_band + gutter, safe.top),
    }


def place_in(mobject, area: SafeArea, *, align="center"):
    """Translate into a region using measured extents, without changing typography."""
    box = bounds(mobject)
    if box.width > area.width + 1e-6 or box.height > area.height + 1e-6:
        raise LayoutError(f"Object {box.width:.3f}x{box.height:.3f} exceeds region "
                          f"{area.width:.3f}x{area.height:.3f}; wrap or split content")
    x = (area.left + area.right - box.left - box.right) / 2
    y = (area.bottom + area.top - box.bottom - box.top) / 2
    if align == "top":
        y = area.top - box.top
    elif align == "bottom":
        y = area.bottom - box.bottom
    elif align != "center":
        raise ValueError("align must be center, top, or bottom")
    mobject.shift([x, y, 0])
    return mobject


def stack_in(mobjects, area: SafeArea, *, gap=0.28, align="top"):
    """Arrange a measured vertical stack atomically; fail before mutating on overflow."""
    items = list(mobjects)
    if gap < 0:
        raise ValueError("gap must be nonnegative")
    boxes = [bounds(m) for m in items]
    height = sum(b.height for b in boxes) + gap * max(0, len(items) - 1)
    if height > area.height + 1e-6 or any(b.width > area.width + 1e-6 for b in boxes):
        raise LayoutError("Stack exceeds region; split into successive beats")
    if align not in {"top", "center", "bottom"}:
        raise ValueError("Unknown stack alignment")
    top = area.top if align == "top" else (
        area.bottom + height if align == "bottom" else (area.top + area.bottom + height) / 2)
    for mob, box in zip(items, boxes):
        place_in(mob, SafeArea(area.left, area.right, top - box.height, top), align="top")
        top -= box.height + gap
    return items


@dataclass
class LayoutItem:
    """Semantic object, not individual glyphs. No blanket containment exemption."""
    id: str
    mobject: object
    region: str = "content"


@dataclass(frozen=True)
class LayoutIssue:
    severity: str
    scene: str
    ids: tuple[str, ...]
    message: str

    def __str__(self):
        return f"{self.severity} [{self.scene}] {', '.join(self.ids)}: {self.message}"


class LayoutValidator:
    """AABB broad-phase audit. Explicit pairs accept panels/highlights/transform overlays.

    Register semantic siblings separately to detect internal collisions. Do not register
    both an entire diagram and its descendants unless containment pairs are declared.
    AABB tests are conservative for diagonal arrows: inspect reported frames manually.
    """

    def __init__(self, regions=None, *, scene="scene", tolerance=0.015, min_gap=0.08):
        self.regions = regions or layout_regions()
        self.scene = scene
        self.tolerance = tolerance
        self.min_gap = min_gap
        self.allowed = {}

    def allow(self, first: str, second: str, *, reason: str):
        if not reason.strip() or first == second:
            raise ValueError("Intentional overlaps need distinct IDs and a reason")
        self.allowed[frozenset((first, second))] = reason

    def validate(self, items):
        items = list(items)
        if len({i.id for i in items}) != len(items):
            raise ValueError("Layout IDs must be unique")
        issues = []
        boxes = {i.id: bounds(i.mobject) for i in items}
        for item in items:
            box = boxes[item.id]
            area = self.regions[item.region]
            outside = box_overflow(box.left, box.right, box.bottom, box.top,
                                   area, tol=self.tolerance)
            if outside:
                issues.append(LayoutIssue("ERROR", self.scene, (item.id,),
                    f"outside {item.region} ({', '.join(outside)}); "
                    "content must stay above the subtitle-safe region"))
        for index, a in enumerate(items):
            for b in items[index + 1:]:
                x, y = boxes[a.id], boxes[b.id]
                dx = min(x.right, y.right) - max(x.left, y.left)
                dy = min(x.top, y.top) - max(x.bottom, y.bottom)
                if dx > self.tolerance and dy > self.tolerance:
                    reason = self.allowed.get(frozenset((a.id, b.id)))
                    issues.append(LayoutIssue("INFO" if reason else "ERROR", self.scene,
                        (a.id, b.id), f"intentional overlap: {reason}" if reason else
                        f"collision ({dx:.3f} x {dy:.3f}); reposition or separate beats"))
                elif dx > -self.min_gap and dy > -self.min_gap:
                    # Tiny penetrations / touching edges aren't obscuration errors.
                    issues.append(LayoutIssue("WARNING", self.scene, (a.id, b.id),
                                              "spacing below minimum gap"))
        return issues


def place_label(label, target, area, *, obstacles=(), gap=0.16):
    """Try right/left/above/below, restoring position and raising if none are safe."""
    from manim import RIGHT, LEFT, UP, DOWN
    original = label.get_center().copy()
    validator = LayoutValidator({"content": area}, min_gap=gap)
    for direction in (RIGHT, LEFT, UP, DOWN):
        label.next_to(target, direction, buff=gap)
        items = [LayoutItem("label", label), LayoutItem("target", target)]
        items += [LayoutItem(f"obstacle-{i}", m) for i, m in enumerate(obstacles)]
        conflicts = [i for i in validator.validate(items) if "label" in i.ids
                     and i.severity != "INFO"]
        if not conflicts:
            return label
    label.move_to(original)
    raise LayoutError("No collision-free label position; reroute arrow or move diagram")
