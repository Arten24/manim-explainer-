# QUONITRON Manim Master Library

An extensible, reusable **Manim Community Edition** animation library with a
searchable JSON catalog, a shared design system, subtitle export, scene
planning helpers, and automated quality checks for educational videos.

This repository is built so AI coding agents and humans can **search, reuse,
configure, and compose** tested components instead of rewriting animations
from scratch.

> Current milestone: **Part 0 — foundation**. Visual animation parts are
> implemented one at a time. See [docs/development-plan.md](docs/development-plan.md).

## What works today

- Design tokens and a swappable `quonitron_dark` theme
- JSON Schema + master catalog with search
- Component metadata + in-memory registry
- Script → scene splitting with catalog query hints
- Subtitle cues with **estimated** timing, SRT, and WebVTT export
- Catalog / syntax / import QA that does **not** require a video render

## What is not claimed yet

- A full motion / math / ML component library
- Voiceover generation or audio alignment
- Successful Manim preview renders in environments without Cairo, Pango,
  and FFmpeg

Estimated subtitle timings are **not** synchronized to a real speaker.

## Install

Python 3.10+ recommended.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

For actual video rendering you also need the Manim system dependencies
(Cairo, Pango, FFmpeg). Follow
[Manim installation](https://docs.manim.community/en/stable/installation.html).

Pinned range: `manim>=0.18.1,<1.0` (compatible with current 0.22 APIs).

## Quick start

```bash
python scripts/validate_catalog.py
python scripts/search_catalog.py "dark theme"
python examples/search_and_subtitles.py
pytest
```

```python
from quonitron.design import get_theme
from quonitron.catalog import search_catalog
from quonitron.subtitles import cues_from_sentences, to_srt

theme = get_theme()
print(theme.color("accent"))

hits = search_catalog("theme")
track = cues_from_sentences(
    ["This library keeps educational animations consistent."],
    scene_id="intro",
)
print(to_srt(track))
```

## Repository layout

```text
quonitron/
  catalog/       JSON catalog, schema, loader, search
  components/    Reusable component base + registry
  design/        Color, type, spacing, motion tokens
  planning/      Script-to-scene helpers
  qa/            Automated checks
  render/        Preview vs production render settings
  scenes/        Scene specs (Manim templates come later)
  subtitles/     Cue model + SRT/WebVTT
docs/            Specification, plan, agent guide
examples/        Runnable examples that do not need Cairo
tests/           Unit tests
scripts/         Catalog validate + search CLIs
```

## Agent workflow

1. Search the catalog for a tested component.
2. Reuse and configure it.
3. Compose.
4. Create a new component only if necessary.
5. Test, then register it. Never mark untested code as tested.

Details: [docs/agent-guide.md](docs/agent-guide.md) and [docs/SPEC.md](docs/SPEC.md).

## License

MIT. See [LICENSE](LICENSE).
