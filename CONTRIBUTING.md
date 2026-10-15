# Contributing

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

For rendering: install Manim system dependencies, then `pip install -e ".[render]"`.

## Checks

```bash
python scripts/validate_catalog.py
pytest -m "not render"
```

## Rules

- One development-plan part at a time.
- Catalog and Python must stay in sync.
- Honest `test_status` values.
- MIT license. Do not commit secrets or bulky generated media.
