# Shared subtitle and animation timeline

Part 2 introduces **one clock** measured in seconds. Subtitle cues and
visual events both store start/end on that clock. Frame numbers are derived
with `timeline.seconds_to_frames(t)` using the configured frame rate.

## Data

See `examples/variable_timeline.json`.

- `scene` — `scene_id`, start, end
- `events` — `id`, `motion_id`, interval, optional `play_duration`,
  `depends_on`, `overlap_ok`, `pause_after`
- `cues` — same fields as Part 1 plus `event_ids` and `timing_status`
- `narration` — full English source text

`play_duration` is the time passed to `Scene.play`. The event interval may
be longer: that is the semantic window used to link cues (the box stays on
screen while later sentences play).

## Linking cues to events

Every animation-linked cue lists one or more `event_ids`. A sentence may
cover several visuals. A long visual may cover several sentences.

Validation (`validate_timeline`):

- scene ids match
- times ≥ 0 and end > start
- cues and events lie inside the scene window
- event ids exist
- accidental overlapping **play** windows are errors unless `overlap_ok`
- missing `event_ids` is a warning

## Estimated vs manual timing

Generated times are `timing_status: estimated`. After you record voiceover,
override without changing cue ids or text:

```python
timeline.override_cue("cue-001", start=0.40, end=2.10)
```

`effective_start()` / `effective_end()` feed SRT, VTT, and the overlay.

If an animation duration changes:

```python
timeline.rescale_event("ev_box", new_duration=1.8, shift_following=True)
validate_timeline(timeline).raise_if_invalid()
```

Manual cues are not shifted.

## Export and inspect

```bash
python scripts/timeline_report.py
```

Writes `examples/variable_timeline_report.md`, `.srt`, and `.vtt` from the
**same** JSON the demo scene loads.

## On-screen captions

`SubtitleOverlay` calls `timeline.cue_at(clock.time)`. The updater uses `dt`
from Manim `play` / `wait`. There is no second hardcoded caption schedule
in the scene.

## After voiceover

1. Keep cue ids and text.
2. Set manual start/end from your take.
3. Re-export SRT/VTT.
4. Re-render only if on-screen captions should follow the new times.
