# Timeline report — assignment_type

- Title: A name for a value
- Scene window: 0.000s → 59.754s (59.754s)
- Frame rate: 30 fps (1793 frames in window)
- Reading speed: 148 wpm (estimates only)
- Events: 17
- Cues: 11
- Beats: 6 (same clock; not a second timeline)
- Notes: Part 4 typography demo. Estimated timings. Content area stays above captions.

## Conceptual beats

| id | title | start | end |
| --- | --- | ---: | ---: |
| `beat-open` | Title | 0.000 | 4.334 |
| `beat-code` | Code line | 4.334 | 8.668 |
| `beat-name` | The name | 8.668 | 20.718 |
| `beat-value` | The value | 20.718 | 32.224 |
| `beat-math` | Replace the value | 32.224 | 42.919 |
| `beat-recap` | Recap | 42.919 | 59.754 |

Cues that continue across a beat boundary:

- None.

## Validation

OK

- No issues.

## Visual events

| id | kind | motion | start | end | play | src | dest |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `ev-title` | motion | `motion.appearance.fade_in` | 0.250 | 4.334 | 1.100 | — | — |
| `ev-heading` | motion | `motion.appearance.write` | 1.450 | 5.134 | 1.150 | — | — |
| `ev-sub` | motion | `motion.appearance.fade_in` | 2.700 | 5.834 | 0.800 | — | — |
| `ev-code` | motion | `motion.appearance.write` | 4.534 | 14.218 | 1.200 | — | — |
| `ev-name` | motion | `text.highlighted_phrase` | 8.818 | 20.718 | 1.000 | — | — |
| `ev-indicate-name` | motion | `motion.emphasis.indicate` | 14.368 | 20.718 | 1.000 | — | — |
| `ev-value` | motion | `text.highlighted_phrase` | 20.868 | 32.224 | 1.000 | — | — |
| `ev-indicate-value` | motion | `motion.emphasis.indicate` | 22.018 | 27.079 | 1.000 | — | — |
| `ev-note` | motion | `text.annotation` | 27.229 | 32.224 | 1.000 | — | — |
| `ev-clear-explain` | motion | `motion.appearance.fade_out` | 31.524 | 32.224 | 0.550 | — | — |
| `ev-equation` | motion | `text.equation` | 32.274 | 42.919 | 1.000 | — | — |
| `ev-counter` | motion | `text.counter` | 33.374 | 42.919 | 0.850 | — | — |
| `ev-replace` | motion | `motion.transform.replacement` | 37.925 | 42.919 | 1.100 | — | — |
| `ev-clear-code` | motion | `motion.appearance.fade_out` | 42.219 | 42.919 | 0.550 | — | — |
| `ev-steps` | motion | `text.step_list` | 43.069 | 58.354 | 1.050 | — | — |
| `ev-recap` | motion | `text.bullet_list` | 47.404 | 58.354 | 1.050 | — | — |
| `ev-body` | motion | `text.paragraph` | 52.548 | 58.354 | 1.000 | — | — |

## Subtitle cues

| id | seq | status | start | end | event_ids | text |
| --- | ---: | --- | ---: | ---: | --- | --- |
| `cue-001` | 1 | estimated | 0.000 | 4.334 | ev-title, ev-heading | A variable is a name that points at a value. |
| `cue-002` | 2 | estimated | 4.334 | 8.668 | ev-code | We write that idea in code as score equals ten. |
| `cue-003` | 3 | estimated | 8.668 | 14.218 | ev-name | Look at the left-hand side: the word score is the name we chose. |
| `cue-004` | 4 | estimated | 14.218 | 20.718 | ev-indicate-name | That name is not the number itself; it is how we will find the number later. |
| `cue-005` | 5 | estimated | 20.718 | 27.079 | ev-value, ev-indicate-value | Now look at the right-hand side: ten is the value sitting in that named slot. |
| `cue-006` | 6 | estimated | 27.079 | 32.224 | ev-note | An annotation helps: the name stays put even when the number changes. |
| `cue-007` | 7 | estimated | 32.224 | 37.775 | ev-equation, ev-counter | We can write the same fact as a compact equation, score equals ten. |
| `cue-008` | 8 | estimated | 37.775 | 42.919 | ev-replace | If the program later assigns eleven, only the stored value is replaced. |
| `cue-009` | 9 | estimated | 42.919 | 47.254 | ev-steps | The identifier score still labels the same slot in memory. |
| `cue-010` | 10 | estimated | 47.254 | 52.398 | ev-recap | So remember three pieces: a name, a slot, and a replaceable value. |
| `cue-011` | 11 | estimated | 52.398 | 58.354 | ev-body | Keep the spoken captions low on the frame, and the lesson text above them. |

## Compiled schedule

- t=  0.000s  cue_start     cue-001  {'text': 'A variable is a name that points at a value.', 'end': 4.334}
- t=  0.250s  event_start   ev-title  {'motion_id': 'motion.appearance.fade_in', 'end': 4.334, 'run_time': 1.1, 'play_end': 1.35, 'label': ''}
- t=  1.450s  event_start   ev-heading  {'motion_id': 'motion.appearance.write', 'end': 5.1339999999999995, 'run_time': 1.15, 'play_end': 2.5999999999999996, 'label': ''}
- t=  2.700s  event_start   ev-sub  {'motion_id': 'motion.appearance.fade_in', 'end': 5.834, 'run_time': 0.8, 'play_end': 3.5, 'label': ''}
- t=  4.334s  cue_end       cue-001  {}
- t=  4.334s  event_end     ev-title  {'motion_id': 'motion.appearance.fade_in'}
- t=  4.334s  cue_start     cue-002  {'text': 'We write that idea in code as score equals ten.', 'end': 8.668}
- t=  4.534s  event_start   ev-code  {'motion_id': 'motion.appearance.write', 'end': 14.218, 'run_time': 1.2, 'play_end': 5.734, 'label': ''}
- t=  5.134s  event_end     ev-heading  {'motion_id': 'motion.appearance.write'}
- t=  5.834s  event_end     ev-sub  {'motion_id': 'motion.appearance.fade_in'}
- t=  8.668s  cue_end       cue-002  {}
- t=  8.668s  cue_start     cue-003  {'text': 'Look at the left-hand side: the word score is the name we chose.', 'end': 14.218}
- t=  8.818s  event_start   ev-name  {'motion_id': 'text.highlighted_phrase', 'end': 20.718, 'run_time': 1.0, 'play_end': 9.818, 'label': ''}
- t= 14.218s  cue_end       cue-003  {}
- t= 14.218s  event_end     ev-code  {'motion_id': 'motion.appearance.write'}
- t= 14.218s  cue_start     cue-004  {'text': 'That name is not the number itself; it is how we will find the number later.', 'end': 20.718}
- t= 14.368s  event_start   ev-indicate-name  {'motion_id': 'motion.emphasis.indicate', 'end': 20.718, 'run_time': 1.0, 'play_end': 15.368, 'label': ''}
- t= 20.718s  cue_end       cue-004  {}
- t= 20.718s  event_end     ev-indicate-name  {'motion_id': 'motion.emphasis.indicate'}
- t= 20.718s  event_end     ev-name  {'motion_id': 'text.highlighted_phrase'}
- t= 20.718s  cue_start     cue-005  {'text': 'Now look at the right-hand side: ten is the value sitting in that named slot.', 'end': 27.079}
- t= 20.868s  event_start   ev-value  {'motion_id': 'text.highlighted_phrase', 'end': 32.224, 'run_time': 1.0, 'play_end': 21.868, 'label': ''}
- t= 22.018s  event_start   ev-indicate-value  {'motion_id': 'motion.emphasis.indicate', 'end': 27.079, 'run_time': 1.0, 'play_end': 23.018, 'label': ''}
- t= 27.079s  cue_end       cue-005  {}
- t= 27.079s  event_end     ev-indicate-value  {'motion_id': 'motion.emphasis.indicate'}
- t= 27.079s  cue_start     cue-006  {'text': 'An annotation helps: the name stays put even when the number changes.', 'end': 32.224}
- t= 27.229s  event_start   ev-note  {'motion_id': 'text.annotation', 'end': 32.224, 'run_time': 1.0, 'play_end': 28.229, 'label': ''}
- t= 31.524s  event_start   ev-clear-explain  {'motion_id': 'motion.appearance.fade_out', 'end': 32.224, 'run_time': 0.55, 'play_end': 32.074, 'label': ''}
- t= 32.224s  cue_end       cue-006  {}
- t= 32.224s  event_end     ev-clear-explain  {'motion_id': 'motion.appearance.fade_out'}
- t= 32.224s  event_end     ev-note  {'motion_id': 'text.annotation'}
- t= 32.224s  event_end     ev-value  {'motion_id': 'text.highlighted_phrase'}
- t= 32.224s  cue_start     cue-007  {'text': 'We can write the same fact as a compact equation, score equals ten.', 'end': 37.775}
- t= 32.274s  event_start   ev-equation  {'motion_id': 'text.equation', 'end': 42.919, 'run_time': 1.0, 'play_end': 33.273999999999994, 'label': ''}
- t= 33.374s  event_start   ev-counter  {'motion_id': 'text.counter', 'end': 42.919, 'run_time': 0.85, 'play_end': 34.224, 'label': ''}
- t= 37.775s  cue_end       cue-007  {}
- t= 37.775s  cue_start     cue-008  {'text': 'If the program later assigns eleven, only the stored value is replaced.', 'end': 42.919}
- t= 37.925s  event_start   ev-replace  {'motion_id': 'motion.transform.replacement', 'end': 42.919, 'run_time': 1.1, 'play_end': 39.025, 'label': ''}
- t= 42.219s  event_start   ev-clear-code  {'motion_id': 'motion.appearance.fade_out', 'end': 42.919, 'run_time': 0.55, 'play_end': 42.76899999999999, 'label': ''}
- t= 42.919s  cue_end       cue-008  {}
- t= 42.919s  event_end     ev-clear-code  {'motion_id': 'motion.appearance.fade_out'}
- t= 42.919s  event_end     ev-counter  {'motion_id': 'text.counter'}
- t= 42.919s  event_end     ev-equation  {'motion_id': 'text.equation'}
- t= 42.919s  event_end     ev-replace  {'motion_id': 'motion.transform.replacement'}
- t= 42.919s  cue_start     cue-009  {'text': 'The identifier score still labels the same slot in memory.', 'end': 47.254}
- t= 43.069s  event_start   ev-steps  {'motion_id': 'text.step_list', 'end': 58.354, 'run_time': 1.05, 'play_end': 44.11899999999999, 'label': ''}
- t= 47.254s  cue_end       cue-009  {}
- t= 47.254s  cue_start     cue-010  {'text': 'So remember three pieces: a name, a slot, and a replaceable value.', 'end': 52.398}
- t= 47.404s  event_start   ev-recap  {'motion_id': 'text.bullet_list', 'end': 58.354, 'run_time': 1.05, 'play_end': 48.45399999999999, 'label': ''}
- t= 52.398s  cue_end       cue-010  {}
- t= 52.398s  cue_start     cue-011  {'text': 'Keep the spoken captions low on the frame, and the lesson text above them.', 'end': 58.354}
- t= 52.548s  event_start   ev-body  {'motion_id': 'text.paragraph', 'end': 58.354, 'run_time': 1.0, 'play_end': 53.548, 'label': ''}
- t= 58.354s  cue_end       cue-011  {}
- t= 58.354s  event_end     ev-body  {'motion_id': 'text.paragraph'}
- t= 58.354s  event_end     ev-recap  {'motion_id': 'text.bullet_list'}
- t= 58.354s  event_end     ev-steps  {'motion_id': 'text.step_list'}

## Narration (source of truth)

A variable is a name that points at a value.
We write that idea in code as score equals ten.
Look at the left-hand side: the word score is the name we chose.
That name is not the number itself; it is how we will find the number later.
Now look at the right-hand side: ten is the value sitting in that named slot.
An annotation helps: the name stays put even when the number changes.
We can write the same fact as a compact equation, score equals ten.
If the program later assigns eleven, only the stored value is replaced.
The identifier score still labels the same slot in memory.
So remember three pieces: a name, a slot, and a replaceable value.
Keep the spoken captions low on the frame, and the lesson text above them.
