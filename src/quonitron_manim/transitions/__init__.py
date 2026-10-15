"""Part 3 transition library."""

from quonitron_manim.transitions.base import DIRECTIONS, TransitionRecipe
from quonitron_manim.transitions.camera import (
    CloseUpToFullTransition,
    PanTransition,
    ReframeTransition,
    ZoomInTransition,
    ZoomOutTransition,
    camera_available,
)
from quonitron_manim.transitions.continuity import (
    CarryAnchorTransition,
    MatchShapesTransition,
    MorphTransition,
    ReplaceTransition,
    RoleShiftTransition,
    SimplifyToDetailTransition,
)
from quonitron_manim.transitions.simple import (
    CoverTransition,
    CutTransition,
    DirectionalRevealTransition,
    FadeTransition,
    GroupSwapTransition,
    SequentialRevealTransition,
    ShapeRevealTransition,
    SlideTransition,
    UncoverTransition,
    WipeTransition,
)
from quonitron_manim.transitions.story import (
    ChapterBreak,
    ClosingPreview,
    CodeToMemory,
    CodeToTrace,
    DiagramToChart,
    ExampleToCode,
    ExplanationToExample,
    ExplanationToRecap,
    TitleToExplanation,
)

ALL_TRANSITIONS = [
    FadeTransition,
    CutTransition,
    SlideTransition,
    WipeTransition,
    CoverTransition,
    UncoverTransition,
    DirectionalRevealTransition,
    ShapeRevealTransition,
    SequentialRevealTransition,
    GroupSwapTransition,
    MorphTransition,
    MatchShapesTransition,
    ReplaceTransition,
    RoleShiftTransition,
    SimplifyToDetailTransition,
    CarryAnchorTransition,
    ZoomInTransition,
    ZoomOutTransition,
    PanTransition,
    ReframeTransition,
    CloseUpToFullTransition,
    TitleToExplanation,
    ExplanationToExample,
    ExampleToCode,
    CodeToTrace,
    CodeToMemory,
    DiagramToChart,
    ExplanationToRecap,
    ChapterBreak,
    ClosingPreview,
]


def search_transitions(
    query: str = "",
    *,
    direction: str | None = None,
    camera: bool | None = None,
    subcategory: str | None = None,
):
    """Filter registered transition classes for agent selection."""
    tokens = [t for t in query.lower().split() if t]
    hits = []
    for cls in ALL_TRANSITIONS:
        blob = " ".join(
            [
                cls.component_id,
                cls.name,
                cls.subcategory,
                cls.description or "",
                " ".join(cls.tags),
                " ".join(cls.aliases),
                " ".join(cls.use_cases),
            ]
        ).lower()
        if tokens and not all(token in blob for token in tokens):
            continue
        if subcategory and cls.subcategory != subcategory:
            continue
        if camera is True and not cls.needs_moving_camera:
            continue
        if camera is False and cls.needs_moving_camera:
            continue
        if direction:
            schema = cls.parameters_schema or {}
            if "direction" not in schema and direction.lower() not in blob:
                continue
        hits.append(cls)
    return hits


__all__ = ["ALL_TRANSITIONS", "DIRECTIONS", "TransitionRecipe", "search_transitions"] + [
    cls.__name__ for cls in ALL_TRANSITIONS
]
