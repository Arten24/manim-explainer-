# Architecture

```
script ──► planning.split_script
              │
              ▼
        PlannedScene[] ──► catalog.search_catalog
              │                    │
              ▼                    ▼
        SceneSpec          ComponentMeta / Python class
              │                    │
              ├─ subtitles.cues_from_sentences ──► SRT / VTT
              │
              └─ later: Manim Scene + components ──► preview render
                                                       │
                                                       ▼
                                                     qa checks
```

## Boundaries

- **Catalog JSON** describes what exists. It does not execute animations.
- **Python components** implement behavior. They must stay importable.
- **Design tokens** are the only source of brand color, type, and motion.
- **Subtitles** can be regenerated without re-rendering video.
- **QA** must fail closed on broken IDs, invalid JSON, and missing modules.

## Search

Agents should query by concept, not by filename:

```text
python scripts/search_catalog.py "gradient descent"
python scripts/search_catalog.py "camera zoom" --category camera
python scripts/search_catalog.py linked --tag "data-structure"
```

Foundation catalog entries are limited to the design theme and the base
component. Later parts add entries only after tests exist.
