"""Part 2 basic motion library."""

from quonitron_manim.motion.appearance import (
    CreateMotion,
    DrawBorderThenFillMotion,
    FadeInMotion,
    FadeOutMotion,
    GrowFromCenterMotion,
    GrowFromPointMotion,
    SmoothEntranceMotion,
    SmoothExitMotion,
    StaggeredRevealMotion,
    UncreateMotion,
    WriteMotion,
)
from quonitron_manim.motion.base import MotionError, MotionRecipe
from quonitron_manim.motion.emphasis import (
    CircumscribeMotion,
    FlashMotion,
    FocusOnMotion,
    FocusSetMotion,
    HighlightLineMotion,
    IndicateMotion,
    PulseMotion,
    WiggleMotion,
)
from quonitron_manim.motion.math_utils import (
    ChangingDecimalMotion,
    CreateLineMotion,
    DotAlongLineMotion,
    MoveArrowMotion,
    TracedPathMotion,
)
from quonitron_manim.motion.position import (
    EnterFrameMotion,
    ExitFrameMotion,
    FollowPathMotion,
    MoveAlongPathMotion,
    MoveBetweenAnchorsMotion,
    MoveGroupMotion,
    MoveToMotion,
    ShiftMotion,
    TrackLabelMotion,
)
from quonitron_manim.motion.rotation import (
    GrowShrinkMotion,
    RotateAndMoveMotion,
    RotateAroundMotion,
    RotateMotion,
    ScaleMotion,
)
from quonitron_manim.motion.sequence import (
    ParallelMotion,
    SequentialMotion,
    StaggeredGroupMotion,
    WaitMotion,
)
from quonitron_manim.motion.transform import (
    FadeTransformMotion,
    MorphPropertyMotion,
    ReplacementTransformMotion,
    TransformMatchingShapesMotion,
    TransformMatchingTexMotion,
    TransformMotion,
)

ALL_MOTION_RECIPES = [
    FadeInMotion,
    FadeOutMotion,
    CreateMotion,
    UncreateMotion,
    WriteMotion,
    DrawBorderThenFillMotion,
    GrowFromCenterMotion,
    GrowFromPointMotion,
    SmoothEntranceMotion,
    SmoothExitMotion,
    StaggeredRevealMotion,
    MoveToMotion,
    ShiftMotion,
    MoveAlongPathMotion,
    FollowPathMotion,
    MoveBetweenAnchorsMotion,
    MoveGroupMotion,
    EnterFrameMotion,
    ExitFrameMotion,
    TrackLabelMotion,
    TransformMotion,
    ReplacementTransformMotion,
    TransformMatchingShapesMotion,
    TransformMatchingTexMotion,
    FadeTransformMotion,
    MorphPropertyMotion,
    IndicateMotion,
    CircumscribeMotion,
    FlashMotion,
    WiggleMotion,
    PulseMotion,
    FocusOnMotion,
    HighlightLineMotion,
    FocusSetMotion,
    RotateMotion,
    RotateAroundMotion,
    ScaleMotion,
    GrowShrinkMotion,
    RotateAndMoveMotion,
    SequentialMotion,
    ParallelMotion,
    StaggeredGroupMotion,
    WaitMotion,
    CreateLineMotion,
    MoveArrowMotion,
    DotAlongLineMotion,
    TracedPathMotion,
    ChangingDecimalMotion,
]

__all__ = ["ALL_MOTION_RECIPES", "MotionError", "MotionRecipe"] + [
    cls.__name__ for cls in ALL_MOTION_RECIPES
]
