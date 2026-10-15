# QUONITRON Manim Master Library

An extensible, reusable **Manim Community Edition** library for educational
videos: a searchable JSON catalog, a shared design system, a base scene,
subtitle export, and automated checks.

The package name is `quonitron_manim`. Agents should **search the catalog
and reuse tested components** before writing new animation code.

Current milestone: **Part 4 — text and typography**.
Parts 5–20 are not implemented.

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
  components/        foundation + Part 4 text blocks
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
│   ├── text_typography_demo.py
│   ├── variable_timeline.json
│   ├── journey_timeline.json
│   └── text_timeline.json
├── notebooks/
│   └── part04_text_typography_demo.ipynb
├── tests/
├── scripts/
│   ├── validate_catalog.py
│   ├── timeline_report.py
│   ├── render_demo.py
│   └── render_motion_demo.py
└── docs/
```

## Setup

The package permits Python **3.10+** and `manim>=0.18.1,<1.0`; that broad range
is not a claim of render verification for every release. The dedicated rendering
reference stack is **Python 3.11, Manim CE 0.19.0, NumPy 2.2.6**.

### Windows + VS Code Jupyter (recommended)

Use the dedicated Conda-forge environment, not a mixture of Conda DLLs and pip
render dependencies. See **[exact Windows setup commands](docs/WINDOWS_SETUP.md)**.

```powershell
# From a Miniforge-enabled PowerShell, in this project folder:
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup_windows.ps1
```

This refuses to replace an existing environment of the same name. Select its
QUONITRON kernel and open `notebooks/environment_render_test.ipynb`. The notebook
fails clearly on a blocked render and embeds actual MP4s after verification.
Windows installation and browser playback must still be verified on your PC;
see [the actual cloud capabilities](docs/CLOUD_CAPABILITIES.md).

### Linux / WSL2

Install native dependencies first (Debian/Ubuntu):

```bash
sudo apt-get update
sudo apt-get install -y libcairo2-dev libpango1.0-dev pkg-config python3-dev python3-venv ffmpeg fonts-dejavu-core
# Choose a fresh name; do not replace an existing working environment.
python3.11 -m venv .venv-render
source .venv-render/bin/activate
python -m pip install -r requirements-render.txt
python -m pip install --no-deps -e .
python scripts/verify_environment.py
python scripts/verify_renders.py --only minimal themed
```

On **0.19.0**, PyAV encodes Manim video; the separate FFmpeg CLI is needed for
this repository's render tests and frame extraction. Cairo/Pango are needed for
these text-based demos. LaTeX is optional because EquationText has a Text fallback.
The Windows Conda route supplies native runtime libraries without requiring
`pkg-config` or a C compiler. Linux pip source builds do need development headers.

For non-rendering work only, `python -m pip install -e ".[dev]"` remains available;
Cairo/Pango/FFmpeg are not required for catalog, timeline and subtitle unit tests.

## Tests

Inexpensive checks (no renderer):

```bash
python scripts/validate_catalog.py
python scripts/timeline_report.py examples/journey_timeline.json --out examples/journey_timeline_report.md
python scripts/search_catalog.py --category transition wipe
python scripts/search_catalog.py --category text paragraph
pytest -m "not render"
```

Preview-render test (needs Cairo, Pango, FFmpeg, Manim):

```bash
pytest -m render
python scripts/render_demo.py
python scripts/render_motion_demo.py
python scripts/render_transition_demo.py
python scripts/render_text_demo.py
```

GitHub Actions runs the unit job on Python 3.10–3.12. The render job is
required to pass; render failures are no longer marked `continue-on-error`.

## Render the demos

From the repository root:

```bash
manim -ql examples/foundation_demo.py VariableStoresAValue
manim -ql examples/motion_timeline_demo.py VariableMemoryTimeline
manim -ql examples/journey_demo.py CodeToMemoryJourney
manim -ql examples/text_typography_demo.py AssignmentInType
```

`-ql` is 480p15 and is the intended smoke render. Do not use `-qh` for
routine tests. Output lands under `media/` (gitignored).

Part 2 loads `examples/variable_timeline.json` for **both** animation
`run_time` values and on-screen captions. Export the same cues with
`python scripts/timeline_report.py`.

Motion, transitions, and the timeline: [docs/motion-library.md](docs/motion-library.md),
[docs/transitions.md](docs/transitions.md), [docs/timeline.md](docs/timeline.md),
[docs/text-typography.md](docs/text-typography.md).

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

- Parts 5–20 are not built. The category list is a registry, not a fake
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

Do not start Part 5 until Part 4 is reported complete.

## License

MIT. See [LICENSE](LICENSE).
