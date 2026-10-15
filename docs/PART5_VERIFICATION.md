# Part 5 verification record

## Tested implementation and scope

Tested code commit: **cb3c220a30b119d45768714ab16099fe780b9828** on
`arena/9c18e37e-manim-explainer`. This record is a subsequent documentation-only
change; results below belong to that exact code commit, not historical cloud prep.
Only Part 5 synchronization was implemented. No Windows PC configuration or Part 6 work.

## 1. Files

- Canonical timing: `src/quonitron_manim/timeline/{models,validate,player,export_subtitles,__init__}.py`.
- Subtitle model, style, narration planning and exports:
  `src/quonitron_manim/subtitles/{models,validation,segment,export}.py`.
- Existing rendering/layout: `components/foundation/subtitle_overlay.py`,
  `core/{text,base_scene}.py`, `design/layout.py` under the same source package.
- Demo: `examples/subtitle_sync_demo.py`.
- Notebook: `notebooks/part05_subtitle_sync.ipynb`.
- Tests: `tests/test_part5_sync.py`, `tests/test_part5_render.py`.
- Existing verification/catalog tooling: `scripts/{verify_renders,publish_ci_evidence,sync_catalog}.py`,
  new `scripts/execute_part5_notebook.py`, `.github/workflows/cloud-verification.yml`.
- Documentation: `PART5_AUDIT.md`, `PART5_SUBTITLE_SYNC.md`, this record, README;
  existing `catalog/master.json` regenerated (still 103 entries, schema unchanged).

No environment, secret, movie, executed notebook or temporary render is tracked.

## 2. Reuse and compatibility

Audit read the existing Parts 1–4 timing, segmentation, typography, transitions,
layout diagnostics, exports and verification paths before source edits. The written
audit was recorded alongside implementation. LinkedCue/Timeline, SubtitleTrack,
SubtitleOverlay, measured_text, theme tokens, reserved band, LayoutValidator,
reasoned overlap permissions, existing catalog IDs and workflow remain canonical.
Legacy `manual` overrides and standalone track wrapping remain supported.
New safety validation intentionally rejects malformed data previously accepted.

Directly blocking repairs include nested intersection checks, finite/mutated interval
validation, provenance lost in export, multiline preservation, scene-relative clock
binding, individual durations inside overlapping animation batches, and camera-time
AABB projection without deep-copying glyph trees.

Native feedback caught a moved default caption anchor and a demo `next_to` direction
list incompatible with Manim's floating `buff`. Default zero padding preserves the
legacy anchor; the demo now uses Manim `DOWN`. Existing assertions were not weakened.
The final run below passed after both fixes.

## 3. Timeline and caption behavior

Finite positive effective intervals, stable cue IDs, unique sequences, scene/event
references, half-open lookups, explicit gaps, event-derived estimates, manual alignment,
optional audio reference/playback, lead-in/out and JSON metadata roundtrips are covered.
`estimated`, `manually_aligned`, `verified` and legacy `manual` are supported. Verification
is an explicit human attestation requiring notes and an audio reference, never an
automatic inference. No supplied audio means all demo cues remain estimated.

Intentional concurrent narration requires track permission, both cue permissions,
and distinct speakers. The overlay preflights all active combinations, stacks them,
measures Pango lines at fixed font size and fails on width/height/line limits instead
of shrinking. Existing shared diagnostics run on caption/camera changes.

## 4. Export evidence

SRT/VTT share effective canonical times, sorted text and preserved authored linebreaks.
The adapter retains statuses, event links and narration metadata in the track/JSON;
SRT/VTT cannot encode all provenance. Tests cover punctuation, Unicode, literal markup,
empty tracks, ordering, timestamp carry and collapsed millisecond intervals. A separately
installed optional `srt` parser ran in the editing workspace. Native CI does not install
that optional parser; mandatory structural/precision/Unicode tests always execute.
No new runtime or mandatory parser dependency was introduced. Target-player entity
rendering still needs review, especially for SRT.

## 5. Exact test results

| Environment / command | Passed | Failed/errors | Skipped |
|---|---:|---:|---:|
| Editing workspace `pytest -ra` | 113 | 0 | 15 |
| GitHub native full suite, `pytest -ra --timeout=180` | **128** | **0** | **0** |
| Separate native suite, `pytest -m render --timeout=180` | **15** | **0** | **0** |

The 15 native tests are a subset of the 128, not additional unique tests. New Part 5
coverage is 25 nonnative cases and 4 native checks. Native regression coverage includes
Parts 1–4, actual render execution, fixed typography/band containment, multispeaker
preflight, camera projection and overlapping animation durations.

Local skips: 1 environment stack check, 1 foundation render, 6 native layout/camera
checks, 3 Part 2–4 renders, and 4 Part 5 native checks. Missing Manim/Cairo/Pango/FFmpeg
is the reason, not passing render evidence. `compileall` and catalog validation passed;
catalog has 103 components and valid Python references. The Python 3.10/3.11/3.12
unit matrix also passed.

## 6. Actual render evidence

Local actual attempt:
`python -m manim -ql examples/subtitle_sync_demo.py SubtitleSyncDemo` returned **1**,
`No module named manim`. No movie was produced locally.

GitHub native workflow **38786025177 succeeded**:
https://github.com/Arten24/manim-explainer-/actions/runs/38786025177

Separate tests workflow **38786025187 succeeded**:
https://github.com/Arten24/manim-explainer-/actions/runs/38786025187

All **10** verification outputs rendered, fully decoded with FFmpeg, and yielded
nonempty extracted frames: 8 preview scenes (Part 5 plus all existing verification
cases), then themed smoke and Part 5 at **1920×1080, 30 fps**. Part 5 preview MP4 was
66,644 bytes; production MP4 was 159,935 bytes. File sizes alone are not evidence of
correctness; complete decode and frame extraction also succeeded.

API-readable evidence checks:
- Full suite/render manifest: **116601401545** (success).
- Separate native suite: **116600742749** (success).
- Notebook evidence: **116600358186** (success).

Fetch reports and frames reproducibly without artifact redirects:
```sh
python scripts/fetch_ci_evidence.py --sha cb3c220a30b119d45768714ab16099fe780b9828
```
Outputs are ignored under `media/cloud-verification/github/<sha>/`. Full movies and
executed notebooks remain Actions artifacts; no generated video is committed.

## 7. Actual extracted-frame inspection

The agent opened and visually inspected these **actual extracted frames**, not mocks:

| Part 5 sample | Observation |
|---|---|
| Preview 1s | First natural-language caption visible, separated from title/code. |
| Preview 3.7s | Intended blank caption gap; explanation remains visible. |
| Preview 4.5s | Camera is moving; caption remains at the bottom-safe viewport location. |
| Preview 7.5s | Two authored lines visible, punctuation intact, no observed title/code collision. |
| Preview 10.7s | Intended tail gap; no stale recap caption. |
| Production-source 4.5s and 7.5s | Same camera-safe caption and multiline recap behavior; no observed clipping/collision in these samples. |

Production-source frame check IDs **116601540352** and **116601544663** identify
1920×1080 source images. Inspection used the Checks API's JPEG previews (downsampled
for transport), not full-resolution continuous playback. These seven inspected stills
support only their sampled states. They do not prove frame-perfect timing across every
boundary or fix unrelated existing Part 2 hidden labels / Part 3 recap overlap / Part 4
tight typography. No blanket claim that all library overlaps are fixed.

## 8. Notebook execution

Local `python scripts/execute_part5_notebook.py`: **5/5 code cells executed**, 0 errors,
**2 explicit render-dependent skips**, **0 HTML video outputs**. Authoring, validation,
manual-alignment example and SRT/VTT exports ran. Render cells were not successful playback.

Native strict execution: **5/5 code cells executed**, **0 errors**, **0 render skips**,
**1 embedded-video HTML output**. Actual rendering, measured preflight, collision
validation and inline-video generation executed. The existing environment notebook
also passed **9/9 cells**, 0 errors, 7 video HTML outputs. Tracked notebooks remain
output-free; executed copies live under ignored media/. Backend HTML generation does
not certify VS Code/browser frontend playback.

## 9. Remaining limitations / review

- No narration recording supplied, generated or listened to; no speech-verified timings.
- Optional audio wiring tested with a scene double, not a supplied real recording.
- Verified provenance is a caller attestation, not ASR/forced alignment or file authenticity.
- Pango wrapping is display-only; exported words and explicit authored newlines remain
  canonical, while visual line wrapping can differ from external subtitle players.
- Geometry checks cover registered visible semantic objects, not arbitrary unregistered
  internals. AABB tests are conservative; reasoned intentional overlap permissions remain.
- Hiding transitions can obscure captions; validation warns, authors review layers/frames.
- Frame quantization, target SRT/VTT player behavior, continuous motion and frontend video
  playback still require manual review. Finite sample images are not continuous visual signoff.
- Existing unrelated visual defects remain outside Part 5 scope.

## 10. Git outcome

Implementation and native fixes were committed and actually pushed to the session branch:
`53ee0cb`, `7bfa018`, `05b3b1c`, **`cb3c220`**. This verification record is a final
separate documentation-only commit. No branch switch, reset/discard, Windows changes,
Part 6 work, secrets or generated videos were involved.
