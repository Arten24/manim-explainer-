"""In-memory registry of Python component classes."""

from __future__ import annotations

from typing import Dict, List, Optional, Type

from quonitron.components.base import BaseComponent, ComponentMeta


class ComponentRegistry:
    def __init__(self) -> None:
        self._items: Dict[str, Type[BaseComponent]] = {}
        self._meta: Dict[str, ComponentMeta] = {}

    def register(
        self,
        cls: Type[BaseComponent],
        meta: Optional[ComponentMeta] = None,
    ) -> Type[BaseComponent]:
        cid = cls.component_id
        if not cid:
            raise ValueError(f"{cls.__name__} is missing component_id")
        if cid in self._items:
            raise ValueError(f"Component already registered: {cid}")
        resolved = meta or cls.get_meta()
        if resolved.component_id != cid:
            raise ValueError(
                f"Meta id {resolved.component_id!r} does not match class id {cid!r}"
            )
        self._items[cid] = cls
        self._meta[cid] = resolved
        return cls

    def get(self, component_id: str) -> Type[BaseComponent]:
        if component_id not in self._items:
            raise KeyError(f"Unknown component: {component_id}")
        return self._items[component_id]

    def all_ids(self) -> List[str]:
        return sorted(self._items)

    def search(self, query: str) -> List[str]:
        q = query.lower().strip()
        if not q:
            return self.all_ids()
        tokens = q.split()
        hits: List[str] = []
        for cid, meta in self._meta.items():
            blob = meta.search_blob()
            if all(token in blob for token in tokens):
                hits.append(cid)
        return sorted(hits)

    def meta(self, component_id: str) -> ComponentMeta:
        if component_id not in self._meta:
            raise KeyError(f"Unknown component: {component_id}")
        return self._meta[component_id]

    def clear(self) -> None:
        self._items.clear()
        self._meta.clear()


REGISTRY = ComponentRegistry()


def register(cls: Type[BaseComponent], meta: Optional[ComponentMeta] = None):
    REGISTRY.register(cls, meta)
    return cls
