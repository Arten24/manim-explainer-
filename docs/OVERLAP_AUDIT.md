# Parts 1–4 overlap audit and repair

## Status / evidence boundary

Repair code and non-rendering tests completed; **visual acceptance remains blocked**.
No Part 5 or other new Part was started. This audit covers every implemented demo
and the foundation, text, motion, transition, and subtitle components they use.
There are **no visually verified rendered frames** from this sandbox. Do not interpret
passing arithmetic tests or the existing catalog's `test_status` as visual approval.

Environment actually checked: Python 3.11, no Manim, pycairo, manimpango, pkg-config,
or FFmpeg. Installing `.[dev,render]` in `.venv` failed building pycairo: Cairo could
not be resolved without pkg-config. The allowed network does not provide an OS
package repository. Installing `.[dev]` and notebook tools succeeded.

Commands actually run:

- `.venv/bin/pytest`: **81 passed, 9 skipped**. Four existing preview render tests
  and five new real-Manim geometry/dry-render tests skipped for missing dependencies.
- `.venv/bin/python -m compileall -q src examples scripts tests`: passed.
- `.venv/bin/python scripts/render_layout_audit.py`: exit 2, explicitly BLOCKED,
  reporting missing Cairo, Pango, and FFmpeg.
- `.venv/bin/python -m manim -ql examples/text_typography_demo.py AssignmentInType`:
  exit 1, `No module named manim`.
- Executed all cells in `notebooks/overlap_repair_lab.ipynb` with nbclient using
  the installed Python kernel: succeeded; render cells explicitly skipped.
  **Not executed in the VS Code frontend**; embedded video playback is unverified.

## Findings: source-confirmed vs unverified visual risk

| Scope | Actual cause / evidence in original implementation | Repair / remaining verification |
|---|---|---|
| Part 4 `AssignmentInType` | `ev-steps` adds a list at y=0.55; `ev-recap` adds another at y=-0.2 without removing steps; `ev-body` adds text below the recap, also without removing either list. Persistent scene membership is a source-confirmed lifecycle defect. | Steps → recap → body now use sequential fade-out/fade-in swaps. Timeline event IDs, durations and narration are unchanged. Need frame review at 43–54 s. |
| Part 4 headings/content | Title was centered on a top anchor without measuring its top edge; heading/subheading accumulated downward while code and lists used unrelated absolute y coordinates. Annotation and paragraph used `next_to` after their component-level clamp, invalidating that check. | Measured header stack; derived lesson region; phase-aware preflight of co-visible objects. Text beats share the lesson region rather than piling up. Rejects oversize beats before playback. Exact font-dependent appearance not yet verified. |
| Part 1 subtitles | `show_subtitle_text` compressed any overlong single line to frame width. Cue replacement faded two captions in the same location concurrently. | Shared measured wrapping at unchanged caption font size and sequential cue swap. Oversize cues fail with an instruction to split. |
| Parts 2–3 timeline captions | `SubtitleOverlay.build` clamped an initial blank once; `_restyle` width-scaled replacement text and reused the blank's center without checking new height/bottom. | Every cue is measured, wrapped, bottom-aligned in the same reserved band. Geometry errors are not hidden by font shrinking. Need actual cue/frame review. |
| Part 3 moving camera | Caption was an ordinary world-space mobject; zoom targeted a 2.2-unit cell with a frame width near 4.84, with no viewport anchoring. Thus bottom captions could leave the viewport entirely. | Overlay projects its canonical geometry into the current camera viewport on every update. Text remains constant in screen-relative size. Restyling resets to canonical geometry before projection, avoiding cumulative scaling. Needs render review at zoom/restore. |
| Foundation cards | Fixed card sizes and absolute offsets assumed short variable names and values; no interior measurement. Replacement values were unconstrained. | Measured interior stack with padding; actionable overflow on oversized names/values/cards. Replacement value dimensions checked against the current slot. Defaults and object attributes preserved. |
| General text | Character-count wrapping was only a heuristic. Clamp scaled width, then shifted bottom, then top, potentially violating the bottom again if the object was taller than the content region. `max_width` override was not enforced on the final object. | Paragraphs use Pango measurements. Final bounds reject impossible dimensions instead of shifting overflow to another edge. Invalid max_width now raises the intended TextLayoutError rather than an unimported-name error. |
| Foundation title/heading | Text lengths had no frame-width safeguard; fixed spacing didn't account for wrapped titles. | Fixed-size measured wrapping, whole-component placement and explicit overflow. |
| Parts 1–3 layout | Repeated `to_edge`, manual overflow shifts and separate gap choices; no shared final-placement audit. | Consistent content region and spacing; semantic IDs registered for endpoint diagnostics. Part 2 connector endpoints recomputed after reflow. |
| Generic transitions | Fade/carry-anchor/cut intentionally draw incoming/outgoing together. Morph/fade-transform interpolate potentially coincident shapes. Slide recipes can temporarily cross other content; these are not inherently defects for all callers. | Kept generic APIs/semantics intact. Readable sequential swap used where unrelated text shares a region. Other callers must declare intentional pairs or use the readable swap. No rendered claim about transition midpoints. |

**Which scenes are confirmed to look wrong?** None can honestly be certified from
rendered evidence here. Part 4's retained-object bug is confirmed in source. The
remaining findings are deterministic missing safeguards or geometry risks, not
claims that every original rendered cue overlapped. In particular, the Part 2
name-to-value connector was already separated from label endpoints; this audit did
not establish a visible arrow/label collision there.

## Layout system and usage

Improved existing `design/layout.py`; no independent layout framework added.

- `layout_regions`: named `safe`, `content`, `subtitle` rectangles, 0.8-unit margins,
  1.05-unit subtitle band, 0.16-unit separator. `content_area` shares this geometry.
- `bounds`: public Manim `get_left/right/top/bottom`, including a conservative
  minimum footprint for horizontal/vertical connectors.
- `place_in`, `stack_in`: translate without scaling; stacks check fit before
  mutation. Pagination/reflow required if there is insufficient room.
- `place_label`: tries right, left, above, below relative to target; rejects bounds
  and obstacle collisions; restores original position when no candidate works.
- `measured_text`: Pango-measured wrapping, including oversized token splitting and
  explicit paragraph breaks. Too-tall blocks produce actionable `LayoutError`.
- `LayoutValidator`, `LayoutItem`, `LayoutIssue`: semantic stable IDs, ERROR for
  meaningful AABB intersections/bounds violations, WARNING for tight spacing,
  INFO for explicitly accepted overlap. Default intersection tolerance 0.015 units;
  minimum gap 0.08. Tiny contacts are not obscuration errors.

```python
from quonitron_manim.design.layout import LayoutItem, LayoutValidator
validator = LayoutValidator(scene="MyScene")
validator.allow("panel", "label", reason="label deliberately inside background panel")
issues = validator.validate([
    LayoutItem("panel", panel), LayoutItem("label", label),
    LayoutItem("caption", caption, region="subtitle"),
])
for issue in issues:
    print(issue)
```

Register **semantic siblings**, not individual letters. Register a panel and its
text separately and allow that exact pair; unrelated text inside the panel must
still be checked against other text. Intentional containment is never silently
inferred from bounding boxes. Registering a whole diagram checks its external
footprint, not its internal labels: audit those siblings separately when authoring.
Unknown region names and duplicate IDs fail rather than silently bypass validation.

`QuonitronScene.register_layout` plus `check_layout` supports visible-object
checks; scene `play` checks registered visible objects at animation endpoints and
deduplicates warnings. Camera-scene checks project into viewport coordinates.
Part 4 additionally validates mutually exclusive lesson phases **before** playback.
`readable_swap` is an opt-in sequential transition that preserves total run time.

## Files repaired / added

- `src/quonitron_manim/design/layout.py`: regions, placement, semantic validator.
- `src/quonitron_manim/core/text.py`: measured text/subtitle helpers.
- `src/quonitron_manim/core/base_scene.py`: wrapped text helpers, registration,
  diagnostics, sequential swap, common subtitle path.
- Foundation `title_card.py`, `section_heading.py`, `variable_store.py`,
  `subtitle_overlay.py`: measured placement, overflow checks, viewport captions.
- Text `base.py`, `blocks.py`: final geometry guards, measured paragraphs; removed
  paragraph group's self-referential `.lines` assignment.
- All four existing `examples/*demo.py`: repaired placement/lifecycle/registration.
- `examples/layout_audit_demo.py`: repair exercise only, not a new development Part.
- `tests/test_layout_audit.py`: arithmetic, safe bounds, subtitle violations, text
  intersections, intentional containment, tolerances, connector collisions,
  atomic stack failure, notebook gating, optional real geometry/demo dry renders.
- `scripts/render_layout_audit.py`: full-demo renders and timestamped frame capture.
- `notebooks/overlap_repair_lab.ipynb`: executed dependency checks, diagnostics,
  render/display helpers and long-text/diagram/transition examples.

## Required rendered review / known limitations

Run from the repository root in a Cairo/Pango/Manim/FFmpeg environment:

```bash
python -m pip install -e '.[dev,render]'
python -m pytest
python scripts/render_layout_audit.py
```

Open `notebooks/overlap_repair_lab.ipynb` in VS Code and select that same environment.
The notebook uses `tempconfig`, `Scene.render()`, and `Video(filename=..., embed=True)`;
it does not rely on untested notebook magics. Generated video/frames stay in ignored
`media/` directories. The existing Part 4 notebook is retained for compatibility.

Planned representative frame review (NOT completed):

- `VariableStoresAValue`: 1, 5, 12, 20 s, titles/card/subtitle changes.
- `VariableMemoryTimeline`: 5, 34, 59.4, 60, 95 s, connector/value transform/recap.
- `CodeToMemoryJourney`: 10, 22.8, 41, 49, 54, 65 s, morph/zoom/restore/closing.
- `AssignmentInType`: 3, 9, 28, 32, 38.3, 43.5, 47.6, 53 s, dense explanation,
  replacement and old list removal.
- `LayoutRepairExercise`: 1, 3.1, 3.6, 5 s, paragraph, label/arrow, transition.

Remaining manual decisions / risks:

1. **Font-dependent preflight is unverified.** If Part 4 preflight rejects a beat
   on the user's installed fonts, split that beat or use columns. Do not reduce
   subtitle sizes to bypass errors.
2. **Camera close-up intentionally crops surrounding context.** Journey's heading
   and some table cells will leave the viewport during focus. Bounds warnings are
   retained, not blanket-suppressed. Confirm that all essential content at that
   beat (focused value and caption) is visible. Decide whether to widen the shot.
3. Endpoint checks do not prove transition-time safety. The extraction script
   samples transitions, but only a human review can verify their appearance here.
4. AABBs are conservative, especially for diagonal arrows and sparse groups;
   an ERROR means a collision candidate to inspect, not pixel-level proof of
   obscuration. Group-level registration does not inspect all internal subobjects.
5. Single-line code/equations/highlight components intentionally refuse oversize
   content rather than reformatting code or breaking semantic phrase references.
   Long lists and annotations may likewise require manual beat splitting.
6. No pixel-regression baseline was fabricated. Optional Manim tests cover measured
   geometry/dry renders; extraction creates review frames, not screenshot assertions.
7. Plain title anchor helpers remain available for API compatibility; a caller that
   later moves/resizes an object must revalidate final placement. No helper can
   guarantee arbitrary future motion stays within a region.

**Remaining verified accidental collisions:** unknown (no frames available).
The source-confirmed Part 4 persistence defect has been repaired. Visual sign-off
and any font-specific follow-up must precede declaring all overlaps fixed.
Stop here; wait for explicit instruction before any new Part.
