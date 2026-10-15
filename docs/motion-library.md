# Basic motion library (Part 2)

Motion recipes live in `src/quonitron_manim/motion/`. Each recipe has a
stable catalog id, validates parameters without Cairo, and lazily imports
Manim 0.22 when `animate()` is called.

Do **not** use deprecated `ShowCreation`; the library uses `Create`.

## How to choose a component

```bash
python scripts/search_catalog.py fade --category motion
python scripts/search_catalog.py "replacement transform"
python scripts/search_catalog.py indicate
```

Match the educational beat:

| Need | Start with |
| --- | --- |
| Appear / disappear | `motion.appearance.*` |
| Slide or follow a path | `motion.position.*` |
| Change identity or value | `motion.transform.*` |
| Point at something | `motion.emphasis.*` |
| Rotate / scale | `motion.rotation.*` / `motion.scale.*` |
| Several motions as one event | `motion.group.sequential` / `parallel` / `staggered` |
| Hold | `motion.timing.wait` |

## How to configure

```python
from quonitron_manim.motion.appearance import FadeInMotion

anim = FadeInMotion(run_time=0.6, easing="smooth", shift="DOWN").animate(mob)
self.play(anim)
```

If `run_time` is omitted, the theme motion token `speed` (`fast`, `normal`,
`slow`, …) is used. Invalid easings and non-positive durations raise
`MotionError` before Manim is imported.

## How to compose

- Sequential events: separate `VisualEvent` rows on the timeline, or
  `motion.group.sequential` for a single event that plays several animations.
- Parallel: `motion.group.parallel`, or two events with `overlap_ok=true`
  and overlapping *play* windows.
- Staggered group entrance: `motion.appearance.staggered_reveal`.

The Part 2 demo prefers **one VisualEvent per beat** and lets the timeline
player sequence them.

## Renderer notes

- `motion.transform.matching_tex` needs LaTeX.
- `motion.position.track_label` and `motion.util.traced_path` attach
  updaters / tracer mobjects; they are not finite `Scene.play` clips.
- `ShowCreation` is not registered.
