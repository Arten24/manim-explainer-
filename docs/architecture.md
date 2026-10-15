# Architecture

Part 1 establishes the spine later animation parts plug into. Visual
libraries (motion, math, ML, …) are not implemented here.

```
educational script
        │
        ▼
subtitle JSON  ──►  validation  ──►  SRT / WebVTT
        │
        ▼
QuonitronScene (theme, safe area, helpers)
        │
        ├── TitleCard / SectionHeading / VariableStore
        │
        └── catalog/master.json  ──►  search / resolve / QA
```

## Boundaries

| Piece | Responsibility |
| --- | --- |
| `catalog/` | What exists: ids, parameters, test status |
| `src/quonitron_manim/design/` | How it looks: color, type, space, motion |
| `src/quonitron_manim/core/` | Scene contract, catalog loader, component base |
| `src/quonitron_manim/components/` | Reusable building blocks |
| `src/quonitron_manim/subtitles/` | Cue model and file export |
| `examples/` | Runnable demo, not the library itself |

JSON never contains the implementation. Python never is the search index.

## Import path

The installable package is `quonitron_manim` (under `src/`). The repository
root still holds `catalog/`, `examples/`, `tests/`, and `scripts/`.

## Manim

`QuonitronScene` subclasses `manim.Scene` when Cairo is actually usable.
Unit tests that only check catalog JSON, theme tokens, and subtitle export
do not require Cairo, Pango, or FFmpeg.

Do not override `Scene.__init__`. Put theme application in `setup()`.
