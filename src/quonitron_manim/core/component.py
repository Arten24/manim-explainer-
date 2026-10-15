"""Reusable component contract.

Components are not Manim Scene subclasses. They build mobjects (or plain
data) from a Theme plus parameters. Catalog entries point at these classes.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Type

from quonitron_manim.design.theme import Theme, get_theme

ALLOWED_TEST_STATUSES = frozenset({"not_tested", "passed", "failed"})


@dataclass
class ComponentSpec:
    """Runtime view of a catalog row plus the implementing class."""

    component_id: str
    name: str
    version: str
    category: str
    class_ref: Optional[Type["Component"]] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    test_status: str = "not_tested"


class Component:
    """Theme-aware building block.

    Subclasses implement ``build()`` and return a Manim mobject when Manim
    is available. They must not require a Scene until they are added to one.
    """

    component_id: str = "base.component"
    name: str = "Component"
    category: str = "foundation"
    version: str = "0.2.0"

    def __init__(self, theme: Optional[Theme] = None, **params: Any) -> None:
        self.theme = theme or get_theme()
        self.params = params
        self._mobject: Any = None

    def build(self) -> Any:
        raise NotImplementedError(f"{type(self).__name__}.build() is not implemented")

    def get(self) -> Any:
        if self._mobject is None:
            self._mobject = self.build()
        return self._mobject

    def param(self, key: str, default: Any = None) -> Any:
        return self.params.get(key, default)


_REGISTRY: Dict[str, Type[Component]] = {}


def register_component(cls: Type[Component]) -> Type[Component]:
    cid = cls.component_id
    if not cid or cid == "base.component":
        raise ValueError(f"{cls.__name__} needs a unique component_id")
    if cid in _REGISTRY:
        raise ValueError(f"Component already registered: {cid}")
    _REGISTRY[cid] = cls
    return cls


def get_registered(component_id: str) -> Type[Component]:
    if component_id not in _REGISTRY:
        raise KeyError(f"Component {component_id!r} is not registered")
    return _REGISTRY[component_id]


def registered_ids() -> List[str]:
    return sorted(_REGISTRY)


def clear_registry() -> None:
    _REGISTRY.clear()
