# Part 5 integration audit

Source paths were read before implementation (the written audit is recorded alongside
implementation). Baseline: 2c1520a. Scope: synchronization only, not Part 6.

| Existing path | Reuse and directly blocking defects |
|---|---|
| timeline/models, validate, schedule, player | Keep LinkedCue/Timeline, effective seconds, IDs, event links, compile markers, batching and binders. Add finite interval/mutation validation, explicit cue-overlap policy, alignment provenance. Adjacent-only intersection checks missed nested intervals. Preserve legacy `manual` overrides. |
| subtitles/segment (Part 2) | Keep natural-language splitting and protected phrases, add settings validation and event-derived estimates. No speech generation or forced alignment. |
| transition components / Part 3 | Keep transitions and incremental viewport pinning. Captions may cross transitions; same clock governs them. No replacement transition framework. |
| core/text (Part 4) | Keep Pango measurement and theme caption tokens. Add line cap and configurable insets inside existing band; never shrink. |
| design/layout + core/base_scene | Keep shared semantic collision diagnostics and explicit reasoned allow-pairs. Replace per-check glyph copies with projected AABBs so camera-time caption diagnostics are viable. Geometry is not visual signoff. |
| foundation/subtitle_overlay | Extend existing registered overlay, preflight active combinations, show all explicitly overlapping speakers, use scene elapsed time rather than accumulated updater deltas where available. |
| timeline/export_subtitles + subtitles/export | Keep public APIs/adapter, validate canonical timeline, retain statuses/links, chronological output, preserve canonical linebreaks, escape literal markup, reject millisecond collapse and nonfinite times. |
| demos/notebooks/catalog/CI | Add one short demo and notebook, extend existing render evidence workflow. Executable authoring stays in Python. No new component architecture. |

Compatibility: legacy track character wrapping remains default; canonical timeline
exports preserve authored text. New fields have defaults. New safety checks deliberately
reject malformed/nonfinite intervals, unsupported statuses, undeclared caption overlaps,
and unsupported export precision instead of silently producing invalid output.

Existing Part 2 hidden labels, Part 3 recap overlap, and Part 4 tight typography are not
claimed fixed by this work. No supplied audio means no demo cue is speech-verified.
