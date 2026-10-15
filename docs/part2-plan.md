# Part 2 implementation plan

Status: implemented in this milestone. Written before the motion modules
so later work follows the Part 1 architecture instead of replacing it.

## What Part 1 already provides

- Package `quonitron_manim` under `src/`
- Theme tokens, `QuonitronScene`, foundation mobjects
- `catalog/master.json` + JSON Schema 1.0.0 (unchanged shape)
- `SubtitleCue` / `SubtitleTrack`, SRT/WebVTT, overlap policy
- Manim Community Edition declared as `>=0.18.1,<1.0` (0.22.0 APIs)

## Defects left in place (not a redesign)

- `show_subtitle_text` in Part 1 is a one-off caption helper and is **not**
  the timeline clock. Part 2 adds a shared timeline and overlay instead of
  deleting the helper.
- Visual Part 1 catalog rows stay `not_tested` until a real Cairo render
  passes.
- This environment may still lack Cairo/Pango/FFmpeg.

## Part 2 design

1. **Motion recipes** (`quonitron_manim.motion`) wrap Manim 0.22 animations
   (`FadeIn`, `Create`, `Write`, `GrowFromCenter`, `MoveAlongPath`,
   `ReplacementTransform`, `Indicate`, `LaggedStart`, …). They validate
   parameters without constructing a Scene.
2. **Shared timeline** (`quonitron_manim.timeline`) stores scene window,
   visual events, subtitle cues, cue↔event links, estimated vs manual
   timing, and a compile/play adapter.
3. **Segmentation** splits a full narration into readable cues with
   configurable limits. Cue IDs stay stable when only timing is overridden.
4. **Demo** `examples/motion_timeline_demo.py` uses the same JSON timeline
   for on-screen captions, SRT/VTT, and animation `run_time`.

## Manim 0.22 notes

- `ShowCreation` is **not** used (`Create` replaced it).
- `TransformMatchingTex` needs LaTeX; registered with that limitation.
- Overlapping events play as `AnimationGroup` of `Succession(Wait, anim)`.
