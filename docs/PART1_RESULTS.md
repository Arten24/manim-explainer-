# Part 1 verification log

Date: 2026-10-15  
Environment: Debian cloud workspace, Python 3.11.2, pytest 9.1.1, jsonschema 4.26.0  
Manim 0.22.0 is importable only via a local pycairo **stub**. Real Cairo, Pango, and FFmpeg are not installed (apt mirrors were unreachable).

## Commands run

```bash
PYTHONPATH=src python scripts/validate_catalog.py
PYTHONPATH=src pytest -m "not render" -v
PYTHONPATH=src pytest -m render -v
PYTHONPATH=src python scripts/render_demo.py
```

## Results

| Check | Result |
| --- | --- |
| Catalog schema + Python refs | **PASS** (6 components) |
| `pytest -m "not render"` | **24 passed**, 1 deselected |
| `pytest -m render` | **1 skipped** (no real Cairo/Pango/FFmpeg) |
| `python scripts/render_demo.py` | **SKIP** exit 2 — stub pycairo, empty manimpango fonts, no ffmpeg |
| Demo MP4 | **not produced** |

Do not treat visual components as `passed`. They remain `not_tested` in `catalog/master.json`.
