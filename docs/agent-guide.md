# Guide for AI coding agents

Prefer reuse over invention.

1. `python scripts/search_catalog.py "<concept>"`
2. Read `module`, `class_name`, `parameters`, `limitations`, `example`.
3. Configure the existing class with the theme.
4. Create a new component only if the catalog cannot meet the need.
5. Test it. Register it. Never mark it `passed` without tests.

Determinism: seed randomness, use theme tokens, avoid wall-clock timing
in animation logic.
