# Guide for AI coding agents

You are extending a shared library. Prefer reuse over invention.

## Before writing a new animation

1. Run `python scripts/search_catalog.py "<concept>"`.
2. Open the matching Python module listed in `module` / `class_name`.
3. Read `parameters`, `defaults`, `limitations`, and `example`.
4. Configure and compose existing components.
5. Only if nothing fits, add a new component.

## When adding a component

1. Implement it under `quonitron/components/<category>/`.
2. Give it a stable dotted `id` that will never be renamed casually.
3. Add a unit test. Add a lightweight preview render test when Cairo/FFmpeg
   are available.
4. Append an entry to `quonitron/catalog/catalog.json`.
5. Run `python scripts/validate_catalog.py` and `pytest`.
6. Set `test_status` honestly:
   - `untested` — code exists, no checks
   - `syntax_ok` — parses
   - `unit_ok` — unit tests pass
   - `render_ok` — a preview render succeeded
   - `tested` — unit + render + catalog checks passed
7. Never mark untested code as `tested`.
8. Do not break existing parameter names.

## Determinism

Seed any randomness. Avoid wall-clock timing in animation logic. Prefer
theme tokens over raw hex colors and magic durations.
