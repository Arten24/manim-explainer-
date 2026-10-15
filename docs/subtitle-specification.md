# Subtitle specification

Workflow is **subtitle-first**. There is no TTS, no transcription, and no
audio file in Part 1.

## Cue fields

| Field | Required | Meaning |
| --- | --- | --- |
| `id` | yes | Stable cue id |
| `scene_id` | yes | Scene the cue belongs to |
| `sequence` | yes | Order in the scene, starting at 1 |
| `text` | yes | Natural English sentence(s) |
| `start_time` | yes | Seconds, `>= 0` |
| `end_time` | yes | Seconds, strictly after `start_time` |
| `visual_cue` | no | What should be on screen |
| `speaker` | no | Speaker label |

## Track fields

`language`, `reading_wpm`, `min_duration`, `max_duration`, `max_chars`,
`overlap_policy` (`error` | `warn` | `allow`), `notes`, `cues`.

Default overlap policy is `error`.

## Style

Write complete spoken sentences. Do not export keyword soup such as
`variable / box / memory`. A long sentence may be split across cues, but
each cue must still be readable aloud.

## Timing honesty

Times produced from words-per-minute are **estimates**. They are not
aligned to a real speaker. Edit the JSON (or the exported SRT/VTT) when
you record voiceover later. Regenerating subtitles does not require
re-rendering the video, and re-rendering does not require regenerating
subtitles.

## Export

```python
from pathlib import Path
from quonitron_manim.subtitles import load_track, write_srt, write_vtt

track = load_track("examples/subtitle_demo.json")
write_srt(track, Path("examples/subtitle_demo.srt"))
write_vtt(track, Path("examples/subtitle_demo.vtt"))
```

Example source: `examples/subtitle_demo.json` (how a variable stores a value).
