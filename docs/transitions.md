# Transitions (Part 3)

Transitions are `TransitionRecipe` subclasses. They live on the **same**
seconds timeline as Part 2 motion. A conceptual scene change is a `beat`
label, not a second clock.

## How to choose

```bash
python scripts/search_catalog.py --category transition wipe
python scripts/search_catalog.py "code to memory"
python scripts/search_catalog.py "zoom into a selected object"
```

| Need | Start with |
| --- | --- |
| Soft change, no correspondence | `transition.simple.fade` |
| Hard editorial cut | `transition.simple.cut` |
| Keep spatial continuity | `transition.simple.slide` / `cover` / `uncover` |
| Directional bar (may hide captions) | `transition.simple.wipe` |
| Same object, new role | `transition.continuity.morph` / `replace` / `role_shift` |
| Simple model → detailed diagram | `transition.continuity.simplify_to_detail` |
| Zoom / pan | `transition.camera.*` on `QuonitronMovingCameraScene` |
| Lesson shape | `transition.story.*` |

Do not invent a second fade. `transition.simple.fade` composes Part 2
`FadeIn` / `FadeOut`. Morph wraps `motion.transform.transform`.

## Camera

`QuonitronScene` is a plain `manim.Scene`. It has no `camera.frame`.
Camera recipes call `scene.camera.frame.animate` (Manim 0.22
`MovingCameraScene`). Use `QuonitronMovingCameraScene`.

## Subtitles

Cues keep running during a transition. A wipe/cover overlapping a cue is a
**warning** (the line may be unreadable). A cue that spans two beats is
allowed; the clock does not reset.

Demo: `examples/journey_demo.py` + `examples/journey_timeline.json`.
