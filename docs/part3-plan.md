# Part 3 implementation plan

Written against the real Part 1–2 code, not a redesign.

## What already exists

- Theme tokens and `QuonitronScene` (Cairo `Scene`, not a moving camera)
- Part 2 `MotionRecipe` wrappers including Fade, Transform, ReplacementTransform,
  TransformMatchingShapes, LaggedStart, slide-like enter/exit
- One `Timeline` with a single `SceneWindow` and `VisualEvent.motion_id`
- Subtitles on that same clock via `cue_at`

## Defects left in place

- Preview renders still need real Cairo/Pango/FFmpeg
- Part 1 `show_subtitle_text` remains a one-off helper
- Default scenes cannot pan/zoom; camera transitions require
  `QuonitronMovingCameraScene` (`manim.MovingCameraScene`)

## Part 3 design

1. `TransitionRecipe` subclasses `MotionRecipe` with `category="transition"`.
   They compose Part 2 motion where a fade/transform already exists.
2. Timeline gains optional `beats` (conceptual chapters) on the **same**
   seconds clock. A scene change does not reset time.
3. `VisualEvent` gains optional `kind`, `source_id`, `destination_id`,
   `cue_ids` without breaking Part 2 JSON.
4. Continuity validation warns when a wipe/cover overlaps a cue, and when
   a cue spans two beats.
5. Demo: variable card → source line → memory table, with morph, slide/wipe,
   and a camera zoom if MovingCamera is available.

Manim 0.22 camera API used: `self.camera.frame.animate.move_to(...).set(width=...)`
and `Restore(self.camera.frame)`. No invented camera APIs.
