# How to add a component

1. Search the catalog first:

   ```bash
   python scripts/search_catalog.py "variable"
   ```

2. If nothing fits, add a class under `src/quonitron_manim/components/<category>/`.

3. Subclass `Component`, set a stable dotted `component_id`, and implement
   `build()` using the theme:

   ```python
   from quonitron_manim.core.component import Component, register_component

   @register_component
   class Example(Component):
       component_id = "foundation.example"
       name = "Example"
       category = "foundation"
       version = "0.2.0"

       def build(self):
           ...
   ```

4. Use `theme.color("accent")` and `theme.duration("normal")`. Do not
   hard-code brand colors or magic timings.

5. Append a row to `catalog/master.json` with every required schema field.

6. Add a unit test. Add a `@pytest.mark.render` test only if a preview
   render is actually expected.

7. Set `test_status` honestly:

   - `not_tested` — implemented, no passing automated check yet
   - `passed` — the declared tests passed
   - `failed` — tests were run and failed

   Never mark untested visuals as `passed`.

8. Run:

   ```bash
   python scripts/validate_catalog.py
   pytest -m "not render"
   ```

9. Do not rename `id` or public parameter names after a component is
   published. Add new parameters with defaults instead.
