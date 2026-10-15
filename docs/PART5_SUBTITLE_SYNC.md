# Part 5 — subtitle / narration synchronization

## Canonical authoring

`timeline.models.LinkedCue` and `Timeline` remain authoritative. Do not separately
edit a detached SubtitleTrack and expect the scene to change. The existing adapter
`timeline_to_track(timeline)` is an export snapshot, not another authoring clock.

```python
from quonitron_manim.timeline import LinkedCue
cue = LinkedCue(id="explain-score-001", scene_id="assignment", sequence=1,
    text="The name points to a value.", start_time=1, end_time=4,
    event_ids=["reveal-score"], timing_status="estimated",
    timing_source="event_window", lead_in=0.1, lead_out=0.2)
cue.align(1.2, 4.1, notes="Editorial adjustment")  # manually_aligned
# Only after actually listening to a recording:
# cue.align(1.2, 4.1, notes="Reviewed by … against recording …", verified=True,
#           audio_reference="narration.wav")
```

Stable whitespace-free IDs, positive integer sequence, natural English text, scene
and event references, finite positive base/effective intervals are validated. Cues
have optional `speaker`, `visual_cue`, `narration_metadata`, and `alignment_notes`.
`effective_start/end` apply legacy manual overrides and nonnegative lead-in/out.
Padding cannot extend outside the program; transitions and beat crossings are
reported, not silently trimmed. Intervals are half-open `[start,end)`, so boundary
lookups are deterministic and deliberate gaps display no text. Sequence numbers
must be unique. Chronology governs playback/export, not input insertion order.

Statuses: `estimated` is an event-window or reading-speed estimate;
`manually_aligned` is editorial timing; `verified` is a **human attestation** requiring
review notes and `narration_metadata.audio_reference`. The library does not listen
to audio, prove the asset exists, or automatically upgrade status. Legacy `manual`,
`manual_start/end` and `override_timing()` remain supported. `align()` validates an
atomic edit. Event rescaling only changes estimated cues, never aligned/verified cues.

Reuse Part 2 `split_narration`, `pack_cues`, `SegmentSettings`; `cues_for_event` splits
natural narration into deterministic event-ID-derived cues and apportions the event
window using estimated reading weights. Optional gaps and outer padding are explicit.
**These are not forced alignment or measured speaking durations.** Add the resulting
cues to the canonical Timeline and validate its boundaries. Event `cue_ids` references
and cue `event_ids` references are independently checked for existence (not required
to be reciprocally duplicated).

Optional `NarrationAudio(path, start_time, duration)` on Timeline uses Manim's
`add_sound` at the same clock offset. No recording is bundled; missing assets fail
through Manim. Declare duration when known to validate the program end. Audio
playback itself is not a timing-verification algorithm.

## Rendering and layout

`play_on_scene` binds its existing TimelineClock to elapsed scene time relative to
playback start (including a nonzero program origin). Event plays/waits, optional
audio, overlay, compiled markers and exports all use canonical seconds. Frame
quantization still applies; exact cue boundaries need not coincide with frames.
Updater-only test doubles retain dt fallback; final playback clears the overlay.

`SubtitleOverlay` is the existing registered component. `preflight(timeline)`
measures every active cue combination using Part 4 Pango `measured_text` and dark
caption tokens. `SubtitleStyle(max_lines=2, max_width=None, padding=.04,
safe_margin=None, line_gap=.08, speaker_labels=False)` configures layout **inside**
the existing reserved subtitle band. Extra safe margins only inset it. Long tokens
wrap by glyph, explicit line breaks survive, font size never shrinks. Overflow
raises LayoutError asking the author to split a cue, not to hide/crop/shrink it.

Default narration overlap is an error. To intentionally represent simultaneous
voices set Timeline `cue_overlap_policy="allow"`, set **both** cues `overlap_ok=True`,
and supply distinct nonempty speakers. The overlay stacks all active texts and
preflights the combined line count/height. `cues_at` returns all; legacy `cue_at`
returns the first. Optional speaker labels are an overlay presentation choice;
export text remains canonical cue text. Author speaker labels into text if required
in external files.

Existing incremental camera fixation is preserved. Cue changes and moving-camera
updates call existing shared layout checks for registered visible semantic content.
The shared validator projects bounding boxes without copying glyph graphs. Register
important content; unregistered internals cannot be checked. Use existing
`layout_validator.allow(first, second, reason=...)` only for intentional geometric
pairs. Simultaneous narration permission is distinct from geometric overlap.
Warnings do not automatically repair diagrams. Full-screen hiding transitions may
obscure captions; validation warns, and authors must review the actual frame/layer.

## Exports

`write_timeline_subtitles` / `timeline_to_track` validate the canonical timeline and
carry effective times, text, speaker, statuses, provenance and event links to the
existing SubtitleTrack. SRT/VTT use chronological order and millisecond rounding,
reject collapsed sub-millisecond intervals, preserve Unicode, punctuation and
canonical multiline text, and escape `<`, `>` and `&` to avoid interpreted markup.
Some SRT players differ in entity rendering: review the target player. VTT NOTE
metadata is flattened and arrow-safe. Empty tracks produce empty SRT and a VTT
header (plus optional note). JSON roundtrips retain metadata; SRT/VTT formats do
not encode all provenance. Legacy standalone tracks still default to character
wrapping; canonical tracks opt into line preservation. The visible Pango wrapping
may add display lines, but does not change the authored words/text in exports.

## Reproduce and review

```sh
python -m pytest -ra
python scripts/validate_catalog.py
python -m manim -ql examples/subtitle_sync_demo.py SubtitleSyncDemo
python scripts/verify_renders.py --only subtitles
python scripts/verify_renders.py --only subtitles --quality production
python scripts/execute_part5_notebook.py             # explicit render skips allowed
python scripts/execute_part5_notebook.py --strict    # native render required
```

Use existing native dependency setup / requirements-render.txt, not Windows PC
reconfiguration. Open `notebooks/part05_subtitle_sync.ipynb` in the project VS Code
kernel; executable authoring stays in the example/modules. Tracked notebook outputs
stay empty; executed evidence and videos go under ignored media/. Cloud verification
adds this demo to existing render/decode/frame extraction and strict notebook jobs.
No new runtime dependency is required. An optional independent `srt` parser test
runs where already installed; mandatory structural/precision tests always run.

Manual checklist: review t=1 (first cue), 3.7 (gap), 4.5 (moving camera and beat
crossing), 7.5 (multiline recap), 10.7 (tail gap). Verify fixed caption font size,
punctuation, margin containment, contrast, transition continuity, and important
content. Independently listen to actual speech before promoting timing status.
Passing unit tests, geometric assertions, successful rendering, inspected stills,
and interactive frontend playback are separate evidence levels. See
`PART5_VERIFICATION.md` for actual results and limitations of this run.
