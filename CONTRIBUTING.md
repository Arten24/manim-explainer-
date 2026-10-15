# Contributing

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Manim also needs Cairo, Pango, and FFmpeg. See the
[Manim Community installation docs](https://docs.manim.community/en/stable/installation.html).

## Checks

```bash
python scripts/validate_catalog.py
python scripts/search_catalog.py theme
pytest
```

## Rules

- One development-plan part at a time.
- Working code, not empty folders.
- Catalog and Python must stay in sync.
- MIT license. Do not commit secrets or bulky generated media.
