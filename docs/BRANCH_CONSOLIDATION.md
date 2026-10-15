# Selective branch consolidation review

## Scope and provenance

Work directly on approved canonical `arena/9c18e37e-manim-explainer`.
Starting tip: `0f14553290f34d037abec2afdf0d32fde5155dcb`.
Reviewed source: `origin/arena/323e2260-manim-explainer` at
`adb921de68663608a261fe816c26ac1fd766bee7`.
No merge/cherry-pick, new branch, deletion, reset, force-push or main update.
No Part 6 or Part 5 reimplementation. Existing work preserved.

## Decisions after reading actual code

- Adapt `tests/test_example_validation.py`: useful discovery-based checks across all
  three example timeline JSON files plus standalone subtitle_demo.json. Canonical
  tests previously covered individual timelines/exports, not this combined sweep.
  Retain text component IDs in the accepted timeline action registry: Part 4
  deliberately uses them in motion_id. Restricting it to motion/transition recipes
  produced a real failure on text_timeline.json during review; inspection showed
  that restriction was wrong, so the source test's complete registry was retained.
- Adapt `tests/test_notebook_execution.py`: execute all Part 4 authoring notebook
  code cells, validate structure, assert expected timeline output and no errors.
  It does not render or certify playback. Existing canonical strict environment
  and Part 5 notebook checks do not replace this Part 4 authoring regression.
- Review `scripts/verify_render_artifacts.py`: do NOT add a second render/probe
  pipeline. Its useful missing feature is ffprobe stream metadata (codec, dimensions,
  rational frame rate, finite positive duration). Integrate this into the existing
  `scripts/verify_renders.py`, preserving unique output directories, final-scene
  selection, partial-clip exclusion, complete FFmpeg decode, multiple timestamped
  frames, timeouts, logs and honest status fields. Probe failure cannot be counted
  as decoded success. Unit stubs are not claimed as renders.
- Do NOT import `uv.lock`: it resolves a different multi-Python renderer matrix
  (including Manim 0.19.1/0.22.0), not the currently verified Manim 0.19.0 stack.
  Preserve requirements-render.txt pins; no lock-manager migration or runtime
  dependency upgrade. The source branch remains available with its complete lock.
- Reuse only its optional `notebook` dependency extra, so notebook test prerequisites
  are explicit and installable. The existing unit workflow installs that extra on
  Python 3.10/3.11/3.12. Native jobs already install the pinned notebook dependencies.
  No new mandatory runtime dependency.
- Keep the canonical devcontainer and render/cloud workflows; no wholesale replacement.
  README links this decision record; no competing setup guide is introduced.

## Checks

Results will be recorded after execution. Native results from the earlier Part 5
commit must not be represented as results for this integration. Local native stack
is absent; actual render attempts fail with `No module named manim`.
