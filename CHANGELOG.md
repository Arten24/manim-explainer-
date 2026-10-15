# Changelog

## 0.5.0 — 2026-10-15

### Part 4 — text and typography

- 14 `text.*` components (title, heading, paragraph wrap, code line, equation, highlight, lists, counter)
- `content_area()` keeps lesson copy above the subtitle band
- Demo `AssignmentInType` on the shared timeline (`examples/text_timeline.json`)
- Notebook `notebooks/part04_text_typography_demo.ipynb` (no inline Manim magic in this workspace)
- Catalog 1.4.0

## 0.4.0 — 2026-10-15

### Part 3 — transitions

- 30 transition recipes on the shared timeline
- Optional beats; camera recipes need `QuonitronMovingCameraScene`
- Demo `CodeToMemoryJourney`

## 0.3.0 — 2026-10-15

### Part 2 — motion library and shared timeline

- 48 motion recipes wrapping Manim 0.22 APIs (`Create`, not `ShowCreation`)
- Shared `Timeline` with visual events, linked cues, estimated vs manual timing
- Narration segmenter, timeline report, SRT/VTT from the same JSON
- `SubtitleOverlay` driven by `timeline.cue_at`
- Demo `VariableMemoryTimeline` (~34 cues, ~108s estimated)
- Catalog 1.2.0 with 57 real entries

### Notes

- No preview MP4 in the Part 2 cloud environment (Cairo/FFmpeg missing)

## 0.2.0 — 2026-10-15

### Part 1 — foundation

- Move the installable package to `src/quonitron_manim`
- Root `catalog/master.json` + JSON Schema 1.0.0 + `categories.json`
- Design system: `#0D1117` background, semantic roles, type, layout, motion
- `QuonitronScene` with title, heading, caption, and safe-area helpers
- Foundation components: `TitleCard`, `SectionHeading`, `VariableStore`
- Subtitle cues, overlap policy, SRT and WebVTT export
- Demonstration scene `VariableStoresAValue`
- Unit tests and a marked render test
- GitHub Actions workflow `.github/workflows/tests.yml`

### Notes

- Visual components remain `not_tested` until a real Manim preview render passes
- Manim/Cairo is an optional extra so catalog tests can run without system libs

## 0.1.0 — 2026-10-15

- Initial bootstrap under the `quonitron` package (superseded by 0.2.0 layout)
