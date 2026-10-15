"""Part 4 typography components."""

from quonitron_manim.components.text.base import TextComponent
from quonitron_manim.components.text.blocks import (
    BodyParagraph,
    DisplayTitle,
    EducationalCaption,
    SceneHeading,
    Subheading,
)
from quonitron_manim.components.text.code import CodeLine, InlineCode
from quonitron_manim.components.text.emphasis import (
    AnnotationCallout,
    CounterLabel,
    HighlightedPhrase,
    TextStack,
)
from quonitron_manim.components.text.lists import BulletList, StepList
from quonitron_manim.components.text.math import EquationText
from quonitron_manim.components.text.wrap import (
    TextLayoutError,
    chars_for_width,
    highlight_parts,
    wrap_plain_text,
)

ALL_TEXT_COMPONENTS = [
    DisplayTitle,
    SceneHeading,
    Subheading,
    BodyParagraph,
    EducationalCaption,
    InlineCode,
    CodeLine,
    EquationText,
    AnnotationCallout,
    HighlightedPhrase,
    CounterLabel,
    BulletList,
    StepList,
    TextStack,
]

__all__ = [
    "ALL_TEXT_COMPONENTS",
    "TextComponent",
    "TextLayoutError",
    "chars_for_width",
    "highlight_parts",
    "wrap_plain_text",
] + [cls.__name__ for cls in ALL_TEXT_COMPONENTS]
