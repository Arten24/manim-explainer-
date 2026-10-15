# QUONITRON Manim Master Library

An extensible, reusable **Manim Community Edition** library for educational
videos: a searchable JSON catalog, a shared design system, a base scene,
subtitle export, and automated checks.

The package name is `quonitron_manim`. Agents should **search the catalog
and reuse tested components** before writing new animation code.

Current milestone: **Part 3 — reusable transitions on the shared timeline**.
Parts 4–20 are not implemented.

## Purpose

Given an educational script, an author or coding agent should be able to
split it into scenes, search this catalog, compose themed components, export
English subtitles without audio, and render a preview.

## Architecture

```
catalog/master.json  ── searchable index (JSON Schema 1.0.0)
src/quonitron_manim/
  design/            color, type, layout, motion tokens
  core/              base scene, component contract, catalog loader
  motion/            Part 2 animation recipes
  transitions/       Part 3 scene-change recipes
  timeline/          shared subtitle + event clock
  components/        reusable building blocks
  subtitles/         cues, segmentation, SRT / WebVTT
examples/            Part 1 + Part 2 demos and timeline JSON
```

Details: [docs/architecture.md](docs/architecture.md).

## Repository structure

```text
├── README.md
├── LICENSE
├── pyproject.toml
├── manim.cfg
├── catalog/
│   ├── master.json
│   ├── schema.json
│   └── categories.json
├── src/quonitron_manim/
├── examples/
│   ├── foundation_demo.py
│   ├── motion_timeline_demo.py
│   ├── journey_demo.py
│   ├── variable_timeline.json
│   └── journey_timeline.json
├── tests/
├── scripts/
│   ├── validate_catalog.py
│   ├── timeline_report.py
│   ├── render_demo.py
│   └── render_motion_demo.py
└── docs/
```

## Setup

Python **3.10+**. Manim Community Edition **0.18.1–0.22.x** (`manim>=0.18.1,<1.0`).

### Cross-platform (Linux, macOS, Windows)

```bash
git clone <this-repo>
cd quonitron-manim-master-library
python -m venv .venv
```

Linux / macOS:

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

For video rendering you also need Manim’s system libraries (Cairo, Pango,
FFmpeg) and:

```bash
pip install -e ".[dev,render]"
```

Follow the official installer for your OS:
[Manim Community installation](https://docs.manim.community/en/stable/installation.html).

### Windows (PowerShell)

1. Install Python 3.11+ from python.org and tick **Add python.exe to PATH**.
2. Install FFmpeg and add it to PATH.
3. Install Manim’s Windows dependencies as documented upstream
   (Cairo / Pango come in via the Manim install path you choose).
4. Then:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev,render]"
```

If `manim` is not found after install, use `python -m manim`.

A full Cairo/Pango toolchain is **not** required for catalog, theme, and
subtitle unit tests.

## Tests

Inexpensive checks (no renderer):

```bash
python scripts/validate_catalog.py
python scripts/timeline_report.py examples/journey_timeline.json --out examples/journey_timeline_report.md
python scripts/search_catalog.py --category transition wipe
pytest -m "not render"
```

Preview-render test (needs Cairo, Pango, FFmpeg, Manim):

```bash
pytest -m render
python scripts/render_demo.py
python scripts/render_motion_demo.py
python scripts/render_transition_demo.py
```

GitHub Actions runs the unit job on Python 3.10–3.12. The render job is
`continue-on-error` because system packages may fail on a runner.

## Render the demos

From the repository root:

```bash
manim -ql examples/foundation_demo.py VariableStoresAValue
manim -ql examples/motion_timeline_demo.py VariableMemoryTimeline
manim -ql examples/journey_demo.py CodeToMemoryJourney
```

`-ql` is 480p15 and is the intended smoke render. Do not use `-qh` for
routine tests. Output lands under `media/` (gitignored).

Part 2 loads `examples/variable_timeline.json` for **both** animation
`run_time` values and on-screen captions. Export the same cues with
`python scripts/timeline_report.py`.

Motion, transitions, and the timeline: [docs/motion-library.md](docs/motion-library.md),
[docs/transitions.md](docs/transitions.md), [docs/timeline.md](docs/timeline.md).

## Master JSON catalog

`catalog/master.json` is the searchable index. Each entry points at a real
Python class. The loader rejects duplicate ids, unknown categories, broken
related-id references, and missing imports.

```bash
python scripts/search_catalog.py variable
python scripts/search_catalog.py title --category foundation
```

```python
from quonitron_manim.core.catalog import search_catalog, resolve

hits = search_catalog("variable")
VariableStore = resolve("foundation.variable_store")
```

Schema: [docs/catalog-schema.md](docs/catalog-schema.md).

## Add a new component

See [docs/component-authoring.md](docs/component-authoring.md). Short version:
search → implement with the theme → test → register in `master.json` with an
honest `test_status` (`not_tested` / `passed` / `failed`).

## Subtitles

Author cues in JSON (see `examples/subtitle_demo.json`). Export without
touching the video:

```bash
python -c "from pathlib import Path; from quonitron_manim.subtitles import load_track, write_srt, write_vtt; t=load_track('examples/subtitle_demo.json'); write_srt(t, Path('media/demo.srt')); write_vtt(t, Path('media/demo.vtt'))"
```

Timings are **estimates**. They are not aligned to a recorded voice.
No synthetic audio is generated.

Specification: [docs/subtitle-specification.md](docs/subtitle-specification.md).

## Design system

Default background `#0D1117`, primary text `#F5F7FA`, restrained blue accent.
[docs/design-system.md](docs/design-system.md).

## Current limitations

- Parts 4–20 are not built. The category list is a registry, not a fake
  component dump.
- Part 2–3 `animate()` calls need a real Manim renderer. Catalog
  `passed` on those rows means **parameter tests**, not a preview MP4.
- Camera zooms need `QuonitronMovingCameraScene`. Plain `QuonitronScene` cannot pan.
- Visual catalog entries (`foundation.title_card`, `section_heading`,
  `variable_store`, `base_scene`) are `not_tested` until a Manim preview
  render actually passes in the environment that runs the tests.
- This cloud workspace cannot install Cairo/Pango/FFmpeg (apt mirrors are
  unreachable). Unit tests still run. A demo **video render is not claimed**.
- Font faces are fallbacks. Inter is optional.
- Subtitle times are not a real speaker.

## Roadmap (Parts 2–20)

| Part | Focus |
| --- | --- |
| 2 | Basic motion library |
| 3 | Transitions |
| 4 | Text and typography |
| 5 | Full subtitle planner |
| 6 | Shapes and 2D graphics |
| 7 | Charts |
| 8 | Mathematics and geometry |
| 9 | Physics and engineering |
| 10 | Code animation |
| 11 | Data structures and algorithms |
| 12 | AI / ML visuals |
| 13 | Architecture diagrams |
| 14 | Camera and composition |
| 15 | Advanced motion and effects |
| 16 | 3D |
| 17 | Voiceover-ready timing |
| 18 | Full video templates |
| 19 | Automated render QA |
| 20 | Agent integration and catalog expansion |

Do not start Part 4 until Part 3 is reported complete.

## License

MIT. See [LICENSE](LICENSE).
