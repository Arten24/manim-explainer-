"""Base classes for reusable QUONITRON components.

Component metadata lives independently of Manim so the catalog, search, and
QA tools can run without a Cairo/Pango render environment. Visual subclasses
may wrap Manim VGroups in later milestones.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from quonitron.design import Theme, get_theme

ALLOWED_TEST_STATUSES = frozenset(
    {"untested", "syntax_ok", "unit_ok", "render_ok", "tested"}
)


@dataclass
class ComponentMeta:
    """Stable description of a reusable component."""

    component_id: str
    name: str
    category: str
    tags: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    description: str = ""
    module: str = ""
    class_name: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    defaults: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    compatibility: Dict[str, str] = field(default_factory=dict)
    test_status: str = "untested"
    example: str = ""
    limitations: str = ""
    related_ids: List[str] = field(default_factory=list)
    part: int = 0

    def __post_init__(self) -> None:
        if self.test_status not in ALLOWED_TEST_STATUSES:
            raise ValueError(
                f"Invalid test_status {self.test_status!r}. "
                f"Allowed: {sorted(ALLOWED_TEST_STATUSES)}"
            )
        if not self.component_id:
            raise ValueError("component_id is required")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def search_blob(self) -> str:
        parts = [
            self.component_id,
            self.name,
            self.category,
            self.description,
            self.module,
            self.class_name,
            self.limitations,
            " ".join(self.tags),
            " ".join(self.aliases),
            " ".join(self.dependencies),
            " ".join(self.related_ids),
        ]
        return " ".join(parts).lower()


class BaseComponent:
    """Theme-aware component without a hard Manim import.

    Subclasses override ``build`` to construct visual children. Call
    ``ensure_built`` before using those children.
    """

    component_id: str = "base.component"
    name: str = "Base Component"
    category: str = "base"
    tags: List[str] = []
    aliases: List[str] = []
    description: str = "Abstract base for reusable animation components."

    def __init__(self, theme: Optional[Theme] = None, **kwargs: Any) -> None:
        self.theme = theme or get_theme()
        self.kwargs = kwargs
        self._built = False
        self.children: List[Any] = []

    def build(self) -> "BaseComponent":
        self._built = True
        return self

    def ensure_built(self) -> None:
        if not self._built:
            self.build()

    @classmethod
    def get_meta(cls) -> ComponentMeta:
        return ComponentMeta(
            component_id=cls.component_id,
            name=cls.name,
            category=cls.category,
            tags=list(cls.tags),
            aliases=list(cls.aliases),
            description=(cls.description or (cls.__doc__ or "")).strip(),
            module=cls.__module__,
            class_name=cls.__name__,
        )
