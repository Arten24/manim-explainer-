"""Lightweight script-to-scene planning helpers.

This is not a full production planner. It splits an educational script into
logical scenes so later agents can map each scene onto catalog components.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


SCENE_HEADING = re.compile(
    r"^(?:scene\s+\d+[:.)-]\s*|(?:#{1,3}\s+)|(?:part\s+\d+[:.)-]\s*))",
    re.IGNORECASE,
)


@dataclass
class PlannedScene:
    scene_id: str
    title: str
    body: str
    sequence: int
    suggested_queries: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _suggest_queries(title: str, body: str) -> List[str]:
    text = f"{title} {body}".lower()
    hints = []
    catalog_hints = [
        ("gradient descent", "gradient descent"),
        ("neural network", "neural network"),
        ("linked list", "linked list"),
        ("equation", "equation transformation"),
        ("camera", "camera zoom"),
        ("chart", "chart"),
        ("graph", "diagram"),
        ("code", "code animation"),
        ("force", "physics"),
        ("vector", "geometry"),
    ]
    for needle, query in catalog_hints:
        if needle in text:
            hints.append(query)
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{3,}", title.lower())
    if words:
        hints.append(" ".join(words[:4]))
    # Preserve order, drop duplicates.
    seen = set()
    unique = []
    for item in hints:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def split_script(script: str) -> List[PlannedScene]:
    """Split a script into scenes using headings or blank-line groups."""
    lines = script.replace("\r\n", "\n").split("\n")
    chunks: List[List[str]] = []
    current: List[str] = []

    def flush() -> None:
        nonlocal current
        text = "\n".join(current).strip()
        if text:
            chunks.append(current)
        current = []

    for line in lines:
        if SCENE_HEADING.match(line.strip()) and current:
            flush()
            current = [line]
        else:
            current.append(line)
    flush()

    if len(chunks) <= 1:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", script.strip()) if p.strip()]
        if len(paragraphs) > 1:
            chunks = [p.split("\n") for p in paragraphs]

    scenes: List[PlannedScene] = []
    for index, chunk in enumerate(chunks, start=1):
        raw = "\n".join(chunk).strip()
        first, _, rest = raw.partition("\n")
        title = SCENE_HEADING.sub("", first).strip() or f"Scene {index}"
        body = rest.strip() if rest.strip() else raw
        scene_id = f"scene_{index:03d}"
        scenes.append(
            PlannedScene(
                scene_id=scene_id,
                title=title,
                body=body,
                sequence=index,
                suggested_queries=_suggest_queries(title, body),
            )
        )
    return scenes
