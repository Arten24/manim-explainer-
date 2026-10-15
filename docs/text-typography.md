# Text and typography (Part 4)

Typography lives in `src/quonitron_manim/components/text/`. Roles come from
`theme.typography` (`title`, `heading`, `subheading`, `body`, `label`,
`caption`, `code`, `annotation`, `equation`). Hex colors stay in the theme.

Foundation `TitleCard` and `SectionHeading` remain the branded opening and
accent heading. Part 4 adds in-scene copy that **must stay above the subtitle
band** (`design.layout.content_area`).

## Choose a component

```bash
python scripts/search_catalog.py --category text paragraph
python scripts/search_catalog.py "highlighted words"
```

| Need | Start with |
| --- | --- |
| In-scene title | `text.display_title` (or `foundation.title_card`) |
| Section heading | `text.heading` / `foundation.section_heading` |
| Wrapped explanation | `text.paragraph` |
| `score = 10` | `text.code_line` |
| Token in a sentence | `text.inline_code` / `text.highlighted_phrase` |
| Callout | `text.annotation` |
| Equation | `text.equation` (`MathTex`, Text fallback) |
| Recap | `text.bullet_list` / `text.step_list` |
| Number to transform | `text.counter` (`.value_mob`) |

Write-on, fade, indicate, and replacement still use Part 2
`motion.appearance.write`, `fade_in`, `motion.emphasis.indicate`,
`motion.transform.replacement`.

## Timing

Demo clock: `examples/text_timeline.json`. Same JSON drives `play_on_scene`,
on-screen `SubtitleOverlay`, and SRT/VTT.

## Notebook

`notebooks/part04_text_typography_demo.ipynb` — wrapping and catalog cells run
without Cairo. Inline `%%manim` preview is **not** claimed in environments
where IPython / Manim magic is missing. Render with:

```bash
manim -ql examples/text_typography_demo.py AssignmentInType
```
