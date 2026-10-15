# Timeline report — journey

- Title: From code to memory
- Scene window: 0.000s → 70.000s (70.000s)
- Frame rate: 30 fps (2100 frames in window)
- Reading speed: 150 wpm (estimates only)
- Events: 10
- Cues: 11
- Beats: 5 (same clock; not a second timeline)
- Notes: Part 3 journey. Subtitle times are estimates. cue-008 spans the code and memory beats on purpose.

## Conceptual beats

| id | title | start | end |
| --- | --- | ---: | ---: |
| `beat-title` | Title | 0.000 | 12.000 |
| `beat-model` | Simple model | 12.000 | 22.400 |
| `beat-code` | Source line | 22.400 | 44.000 |
| `beat-memory` | Memory table | 44.000 | 58.500 |
| `beat-recap` | Recap | 58.500 | 70.000 |

Cues that continue across a beat boundary:

- `cue-003` 11.760–18.040: That picture is useful, but it is not how the computer actually sees the assignment.
- `cue-004` 18.040–23.120: In source code, the same idea is written as score equals ten.
- `cue-008` 41.600–48.100: The name score is the same in the code and in the table; only the representation changes.
- `cue-010` 52.380–58.880: Zooming back out, the rest of the diagram is still there, and the clock never reset.

## Validation

OK

- **warning** `cue-006` cue-006: no event_ids (narration is not linked to a visual)
- **warning** `cue-003` cue-003: spans more than one conceptual beat (allowed — the clock does not reset at a scene change)
- **warning** `cue-004` cue-004: spans more than one conceptual beat (allowed — the clock does not reset at a scene change)
- **warning** `cue-008` cue-008: spans more than one conceptual beat (allowed — the clock does not reset at a scene change)
- **warning** `cue-010` cue-010: spans more than one conceptual beat (allowed — the clock does not reset at a scene change)

## Visual events

| id | kind | motion | start | end | play | src | dest |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `ev-title-in` | motion | `motion.appearance.fade_in` | 0.400 | 8.000 | 1.200 | — | — |
| `ev-title-to-model` | transition | `transition.story.title_to_explanation` | 9.200 | 12.000 | 1.800 | ev-title-in | ev-write-heading |
| `ev-write-heading` | motion | `motion.appearance.write` | 12.800 | 16.000 | 1.400 | — | — |
| `ev-mark-card` | motion | `motion.emphasis.circumscribe` | 16.400 | 19.500 | 1.200 | — | — |
| `ev-example-to-code` | transition | `transition.story.example_to_code` | 22.400 | 28.000 | 1.800 | ev-mark-card | ev-code-to-memory |
| `ev-code-to-memory` | transition | `transition.story.code_to_memory` | 40.400 | 46.200 | 2.000 | ev-example-to-code | ev-zoom-value |
| `ev-zoom-value` | transition | `transition.camera.zoom_in` | 48.400 | 52.000 | 1.600 | ev-code-to-memory | ev-zoom-full |
| `ev-zoom-full` | transition | `transition.camera.closeup_to_full` | 53.200 | 57.500 | 1.600 | ev-zoom-value | — |
| `ev-to-recap` | transition | `transition.story.explanation_to_recap` | 59.200 | 63.000 | 1.400 | ev-zoom-full | ev-closing |
| `ev-closing` | transition | `transition.story.closing_preview` | 64.400 | 68.500 | 1.500 | ev-to-recap | — |

## Subtitle cues

| id | seq | status | start | end | event_ids | text |
| --- | ---: | --- | ---: | ---: | --- | --- |
| `cue-001` | 1 | estimated | 0.000 | 5.880 | ev-title-in | A variable is a named place that holds a value while a program runs. |
| `cue-002` | 2 | estimated | 5.880 | 11.760 | ev-title-to-model | We start with a simple picture: a box labeled score that currently holds ten. |
| `cue-003` | 3 | estimated | 11.760 | 18.040 | ev-write-heading, ev-mark-card | That picture is useful, but it is not how the computer actually sees the assignment. |
| `cue-004` | 4 | estimated | 18.040 | 23.120 | ev-example-to-code | In source code, the same idea is written as score equals ten. |
| `cue-005` | 5 | estimated | 23.120 | 29.620 | ev-example-to-code | The identifier on the left is the name we chose; the number on the right is the value we stored. |
| `cue-006` | 6 | estimated | 29.620 | 35.100 | — | When this line runs, the language runtime looks up that name in memory. |
| `cue-007` | 7 | estimated | 35.100 | 41.600 | ev-code-to-memory | Memory is just a table of slots: an address, a name, and the value that lives there. |
| `cue-008` | 8 | estimated | 41.600 | 48.100 | ev-code-to-memory | The name score is the same in the code and in the table; only the representation changes. |
| `cue-009` | 9 | estimated | 48.100 | 52.380 | ev-zoom-value | Zooming in, the value cell is where ten actually sits. |
| `cue-010` | 10 | estimated | 52.380 | 58.880 | ev-zoom-full | Zooming back out, the rest of the diagram is still there, and the clock never reset. |
| `cue-011` | 11 | estimated | 58.880 | 65.380 | ev-to-recap, ev-closing | So a variable is not the number itself. It is a stable name for a replaceable slot in memory. |

## Compiled schedule

- t=  0.000s  cue_start     cue-001  {'text': 'A variable is a named place that holds a value while a program runs.', 'end': 5.88}
- t=  0.400s  event_start   ev-title-in  {'motion_id': 'motion.appearance.fade_in', 'end': 8.0, 'run_time': 1.2, 'play_end': 1.6, 'label': ''}
- t=  5.880s  cue_end       cue-001  {}
- t=  5.880s  cue_start     cue-002  {'text': 'We start with a simple picture: a box labeled score that currently holds ten.', 'end': 11.76}
- t=  8.000s  event_end     ev-title-in  {'motion_id': 'motion.appearance.fade_in'}
- t=  9.200s  event_start   ev-title-to-model  {'motion_id': 'transition.story.title_to_explanation', 'end': 12.0, 'run_time': 1.8, 'play_end': 11.0, 'label': ''}
- t= 11.760s  cue_end       cue-002  {}
- t= 11.760s  cue_start     cue-003  {'text': 'That picture is useful, but it is not how the computer actually sees the assignment.', 'end': 18.04}
- t= 12.000s  event_end     ev-title-to-model  {'motion_id': 'transition.story.title_to_explanation'}
- t= 12.000s  pause         ev-title-to-model  {'duration': 0.2}
- t= 12.800s  event_start   ev-write-heading  {'motion_id': 'motion.appearance.write', 'end': 16.0, 'run_time': 1.4, 'play_end': 14.200000000000001, 'label': ''}
- t= 16.000s  event_end     ev-write-heading  {'motion_id': 'motion.appearance.write'}
- t= 16.400s  event_start   ev-mark-card  {'motion_id': 'motion.emphasis.circumscribe', 'end': 19.5, 'run_time': 1.2, 'play_end': 17.599999999999998, 'label': ''}
- t= 18.040s  cue_end       cue-003  {}
- t= 18.040s  cue_start     cue-004  {'text': 'In source code, the same idea is written as score equals ten.', 'end': 23.12}
- t= 19.500s  event_end     ev-mark-card  {'motion_id': 'motion.emphasis.circumscribe'}
- t= 22.400s  event_start   ev-example-to-code  {'motion_id': 'transition.story.example_to_code', 'end': 28.0, 'run_time': 1.8, 'play_end': 24.2, 'label': ''}
- t= 23.120s  cue_end       cue-004  {}
- t= 23.120s  cue_start     cue-005  {'text': 'The identifier on the left is the name we chose; the number on the right is the value we stored.', 'end': 29.62}
- t= 28.000s  event_end     ev-example-to-code  {'motion_id': 'transition.story.example_to_code'}
- t= 28.000s  pause         ev-example-to-code  {'duration': 0.3}
- t= 29.620s  cue_end       cue-005  {}
- t= 29.620s  cue_start     cue-006  {'text': 'When this line runs, the language runtime looks up that name in memory.', 'end': 35.1}
- t= 35.100s  cue_end       cue-006  {}
- t= 35.100s  cue_start     cue-007  {'text': 'Memory is just a table of slots: an address, a name, and the value that lives there.', 'end': 41.6}
- t= 40.400s  event_start   ev-code-to-memory  {'motion_id': 'transition.story.code_to_memory', 'end': 46.2, 'run_time': 2.0, 'play_end': 42.4, 'label': ''}
- t= 41.600s  cue_end       cue-007  {}
- t= 41.600s  cue_start     cue-008  {'text': 'The name score is the same in the code and in the table; only the representation changes.', 'end': 48.1}
- t= 46.200s  event_end     ev-code-to-memory  {'motion_id': 'transition.story.code_to_memory'}
- t= 46.200s  pause         ev-code-to-memory  {'duration': 0.2}
- t= 48.100s  cue_end       cue-008  {}
- t= 48.100s  cue_start     cue-009  {'text': 'Zooming in, the value cell is where ten actually sits.', 'end': 52.38}
- t= 48.400s  event_start   ev-zoom-value  {'motion_id': 'transition.camera.zoom_in', 'end': 52.0, 'run_time': 1.6, 'play_end': 50.0, 'label': ''}
- t= 52.000s  event_end     ev-zoom-value  {'motion_id': 'transition.camera.zoom_in'}
- t= 52.000s  pause         ev-zoom-value  {'duration': 0.4}
- t= 52.380s  cue_end       cue-009  {}
- t= 52.380s  cue_start     cue-010  {'text': 'Zooming back out, the rest of the diagram is still there, and the clock never reset.', 'end': 58.88}
- t= 53.200s  event_start   ev-zoom-full  {'motion_id': 'transition.camera.closeup_to_full', 'end': 57.5, 'run_time': 1.6, 'play_end': 54.800000000000004, 'label': ''}
- t= 57.500s  event_end     ev-zoom-full  {'motion_id': 'transition.camera.closeup_to_full'}
- t= 57.500s  pause         ev-zoom-full  {'duration': 0.2}
- t= 58.880s  cue_end       cue-010  {}
- t= 58.880s  cue_start     cue-011  {'text': 'So a variable is not the number itself. It is a stable name for a replaceable slot in memory.', 'end': 65.38}
- t= 59.200s  event_start   ev-to-recap  {'motion_id': 'transition.story.explanation_to_recap', 'end': 63.0, 'run_time': 1.4, 'play_end': 60.6, 'label': ''}
- t= 63.000s  event_end     ev-to-recap  {'motion_id': 'transition.story.explanation_to_recap'}
- t= 63.000s  pause         ev-to-recap  {'duration': 0.2}
- t= 64.400s  event_start   ev-closing  {'motion_id': 'transition.story.closing_preview', 'end': 68.5, 'run_time': 1.5, 'play_end': 65.9, 'label': ''}
- t= 65.380s  cue_end       cue-011  {}
- t= 68.500s  event_end     ev-closing  {'motion_id': 'transition.story.closing_preview'}
- t= 68.500s  pause         ev-closing  {'duration': 0.4}

## Narration (source of truth)

A variable is a named place that holds a value while a program runs.
We start with a simple picture: a box labeled score that currently holds ten.
That picture is useful, but it is not how the computer actually sees the assignment.
In source code, the same idea is written as score equals ten.
The identifier on the left is the name we chose; the number on the right is the value we stored.
When this line runs, the language runtime looks up that name in memory.
Memory is just a table of slots: an address, a name, and the value that lives there.
The name score is the same in the code and in the table; only the representation changes.
Zooming in, the value cell is where ten actually sits.
Zooming back out, the rest of the diagram is still there, and the clock never reset.
So a variable is not the number itself. It is a stable name for a replaceable slot in memory.
