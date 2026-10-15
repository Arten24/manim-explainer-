# Timeline report — variable_stores_a_value

- Title: How a variable stores a value
- Scene window: 0.000s → 107.995s (107.995s)
- Frame rate: 15 fps (1620 frames in window)
- Reading speed: 165 wpm (estimates only)
- Events: 14
- Cues: 34
- Beats: 0 (same clock; not a second timeline)
- Notes: Estimated timings share this clock with visual events. They are not aligned to a recorded speaker until timing_status is set to manual.

## Validation

OK

- No issues.

## Visual events

| id | kind | motion | start | end | play | src | dest |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `ev_title_in` | motion | `motion.appearance.smooth_entrance` | 0.000 | 2.400 | 1.200 | — | — |
| `ev_title_out` | motion | `motion.appearance.smooth_exit` | 2.400 | 2.900 | 0.500 | — | — |
| `ev_heading` | motion | `motion.appearance.write` | 2.950 | 94.200 | 1.200 | — | — |
| `ev_box` | motion | `motion.appearance.grow_from_center` | 4.250 | 104.400 | 1.200 | — | — |
| `ev_name` | motion | `motion.appearance.write` | 5.550 | 104.400 | 1.050 | — | — |
| `ev_value0` | motion | `motion.appearance.fade_in` | 6.700 | 59.150 | 0.800 | — | — |
| `ev_indicate` | motion | `motion.emphasis.indicate` | 8.000 | 47.200 | 1.150 | — | — |
| `ev_circ_name` | motion | `motion.emphasis.circumscribe` | 27.200 | 33.500 | 1.300 | — | — |
| `ev_arrow` | motion | `motion.util.create_line` | 33.600 | 59.100 | 1.200 | — | — |
| `ev_replace` | motion | `motion.transform.replacement` | 59.150 | 68.650 | 1.250 | — | — |
| `ev_pulse` | motion | `motion.emphasis.pulse` | 68.700 | 71.700 | 1.250 | — | — |
| `ev_focus` | motion | `motion.emphasis.focus_set` | 71.750 | 82.700 | 1.350 | — | — |
| `ev_recap` | motion | `motion.appearance.smooth_entrance` | 94.250 | 104.400 | 1.150 | — | — |
| `ev_end` | motion | `motion.group.parallel` | 104.500 | 107.995 | 1.400 | — | — |

## Subtitle cues

| id | seq | status | start | end | event_ids | text |
| --- | ---: | --- | ---: | ---: | --- | --- |
| `cue-001` | 1 | estimated | 0.000 | 2.342 | ev_title_in | Imagine you are tidying a desk. |
| `cue-002` | 2 | estimated | 2.342 | 6.138 | ev_title_in | You do not throw every paper into one anonymous pile. |
| `cue-003` | 3 | estimated | 6.138 | 11.938 | ev_box | You take a small box, write a name on the lid, and place a single note inside. |
| `cue-004` | 4 | estimated | 11.938 | 14.644 | ev_heading, ev_box | A variable works in that same spirit. |
| `cue-005` | 5 | estimated | 14.644 | 17.966 | ev_heading, ev_box | It is a named place in the computer's memory, |
| `cue-006` | 6 | estimated | 17.966 | 22.126 | ev_heading, ev_box | reserved so your program can find a piece of information again. |
| `cue-007` | 7 | estimated | 22.126 | 25.559 | ev_name, ev_box | The name on the box is not the information. |
| `cue-008` | 8 | estimated | 25.559 | 27.174 | ev_name, ev_box | It is the handle. |
| `cue-009` | 9 | estimated | 27.174 | 31.587 | ev_circ_name, ev_name | When we write the word score, we are pointing at a location, |
| `cue-010` | 10 | estimated | 31.587 | 33.565 | ev_circ_name | not at the number itself. |
| `cue-011` | 11 | estimated | 33.565 | 35.907 | ev_value0, ev_arrow | Inside the box is the value. |
| `cue-012` | 12 | estimated | 35.907 | 38.976 | ev_value0 | That is the information the name currently holds. |
| `cue-013` | 13 | estimated | 38.976 | 43.864 | ev_value0 | At the beginning, score holds zero, because we have not counted anything yet. |
| `cue-014` | 14 | estimated | 43.864 | 45.842 | ev_indicate | Now, here's the important part. |
| `cue-015` | 15 | estimated | 45.842 | 47.252 | ev_indicate | Programs change. |
| `cue-016` | 16 | estimated | 47.252 | 50.575 | ev_box | If we could not change what a box contains, |
| `cue-017` | 17 | estimated | 50.575 | 54.261 | ev_box | we would need a new box for every new number, |
| `cue-018` | 18 | estimated | 54.261 | 57.694 | ev_box | and we would forget where the latest number lives. |
| `cue-019` | 19 | estimated | 57.694 | 59.104 | ev_box | So we reassign. |
| `cue-020` | 20 | estimated | 59.104 | 61.082 | ev_replace | We write score equals ten. |
| `cue-021` | 21 | estimated | 61.082 | 64.515 | ev_replace | We are not creating a second box labeled score. |
| `cue-022` | 22 | estimated | 64.515 | 68.675 | ev_replace | We are opening the same box and replacing the note inside. |
| `cue-023` | 23 | estimated | 68.675 | 70.085 | ev_pulse, ev_name | The name stays. |
| `cue-024` | 24 | estimated | 70.085 | 71.699 | ev_pulse | The value can change. |
| `cue-025` | 25 | estimated | 71.699 | 76.113 | ev_focus | After the assignment, whenever the program asks for score, it receives ten, |
| `cue-026` | 26 | estimated | 76.113 | 77.523 | ev_focus | not zero. |
| `cue-027` | 27 | estimated | 77.523 | 82.774 | ev_box | The visual is helpful: a lid you can read, and contents you can swap. |
| `cue-028` | 28 | estimated | 82.774 | 84.388 | ev_box | It also has limits. |
| `cue-029` | 29 | estimated | 84.388 | 87.094 | ev_box | Real memory is not a wooden crate. |
| `cue-030` | 30 | estimated | 87.094 | 89.689 | ev_box | The computer stores bits at an address, |
| `cue-031` | 31 | estimated | 89.689 | 94.213 | ev_box | and the name is a label your programming language keeps for you. |
| `cue-032` | 32 | estimated | 94.213 | 98.626 | ev_recap | Remember this: a variable binds a stable name to a replaceable value, |
| `cue-033` | 33 | estimated | 98.626 | 104.426 | ev_recap | so the rest of the program can talk about the thing without chasing a moving number. |
| `cue-034` | 34 | estimated | 104.426 | 107.495 | ev_end | That is how a variable stores a value. |

## Compiled schedule

- t=  0.000s  event_start   ev_title_in  {'motion_id': 'motion.appearance.smooth_entrance', 'end': 2.4, 'run_time': 1.2, 'play_end': 1.2, 'label': 'Opening title'}
- t=  0.000s  cue_start     cue-001  {'text': 'Imagine you are tidying a desk.', 'end': 2.342}
- t=  2.342s  cue_end       cue-001  {}
- t=  2.342s  cue_start     cue-002  {'text': 'You do not throw every paper into one anonymous pile.', 'end': 6.138}
- t=  2.400s  event_end     ev_title_in  {'motion_id': 'motion.appearance.smooth_entrance'}
- t=  2.400s  event_start   ev_title_out  {'motion_id': 'motion.appearance.smooth_exit', 'end': 2.9, 'run_time': 0.5, 'play_end': 2.9, 'label': 'Clear title'}
- t=  2.900s  event_end     ev_title_out  {'motion_id': 'motion.appearance.smooth_exit'}
- t=  2.950s  event_start   ev_heading  {'motion_id': 'motion.appearance.write', 'end': 94.2, 'run_time': 1.2, 'play_end': 4.15, 'label': 'Section heading'}
- t=  4.250s  event_start   ev_box  {'motion_id': 'motion.appearance.grow_from_center', 'end': 104.4, 'run_time': 1.2, 'play_end': 5.45, 'label': 'Variable card'}
- t=  5.550s  event_start   ev_name  {'motion_id': 'motion.appearance.write', 'end': 104.4, 'run_time': 1.05, 'play_end': 6.6, 'label': 'Write name score'}
- t=  6.138s  cue_end       cue-002  {}
- t=  6.138s  cue_start     cue-003  {'text': 'You take a small box, write a name on the lid, and place a single note inside.', 'end': 11.938}
- t=  6.700s  event_start   ev_value0  {'motion_id': 'motion.appearance.fade_in', 'end': 59.15, 'run_time': 0.8, 'play_end': 7.5, 'label': 'Value 0'}
- t=  8.000s  event_start   ev_indicate  {'motion_id': 'motion.emphasis.indicate', 'end': 47.2, 'run_time': 1.15, 'play_end': 9.15, 'label': 'Indicate the box'}
- t= 11.938s  cue_end       cue-003  {}
- t= 11.938s  cue_start     cue-004  {'text': 'A variable works in that same spirit.', 'end': 14.644}
- t= 14.644s  cue_end       cue-004  {}
- t= 14.644s  cue_start     cue-005  {'text': "It is a named place in the computer's memory,", 'end': 17.966}
- t= 17.966s  cue_end       cue-005  {}
- t= 17.966s  cue_start     cue-006  {'text': 'reserved so your program can find a piece of information again.', 'end': 22.126}
- t= 22.126s  cue_end       cue-006  {}
- t= 22.126s  cue_start     cue-007  {'text': 'The name on the box is not the information.', 'end': 25.559}
- t= 25.559s  cue_end       cue-007  {}
- t= 25.559s  cue_start     cue-008  {'text': 'It is the handle.', 'end': 27.174}
- t= 27.174s  cue_end       cue-008  {}
- t= 27.174s  cue_start     cue-009  {'text': 'When we write the word score, we are pointing at a location,', 'end': 31.587}
- t= 27.200s  event_start   ev_circ_name  {'motion_id': 'motion.emphasis.circumscribe', 'end': 33.5, 'run_time': 1.3, 'play_end': 28.5, 'label': 'Circumscribe name'}
- t= 31.587s  cue_end       cue-009  {}
- t= 31.587s  cue_start     cue-010  {'text': 'not at the number itself.', 'end': 33.565}
- t= 33.500s  event_end     ev_circ_name  {'motion_id': 'motion.emphasis.circumscribe'}
- t= 33.565s  cue_end       cue-010  {}
- t= 33.565s  cue_start     cue-011  {'text': 'Inside the box is the value.', 'end': 35.907}
- t= 33.600s  event_start   ev_arrow  {'motion_id': 'motion.util.create_line', 'end': 59.1, 'run_time': 1.2, 'play_end': 34.800000000000004, 'label': 'Name to value arrow'}
- t= 35.907s  cue_end       cue-011  {}
- t= 35.907s  cue_start     cue-012  {'text': 'That is the information the name currently holds.', 'end': 38.976}
- t= 38.976s  cue_end       cue-012  {}
- t= 38.976s  cue_start     cue-013  {'text': 'At the beginning, score holds zero, because we have not counted anything yet.', 'end': 43.864}
- t= 43.864s  cue_end       cue-013  {}
- t= 43.864s  cue_start     cue-014  {'text': "Now, here's the important part.", 'end': 45.842}
- t= 45.842s  cue_end       cue-014  {}
- t= 45.842s  cue_start     cue-015  {'text': 'Programs change.', 'end': 47.252}
- t= 47.200s  event_end     ev_indicate  {'motion_id': 'motion.emphasis.indicate'}
- t= 47.252s  cue_end       cue-015  {}
- t= 47.252s  cue_start     cue-016  {'text': 'If we could not change what a box contains,', 'end': 50.575}
- t= 50.575s  cue_end       cue-016  {}
- t= 50.575s  cue_start     cue-017  {'text': 'we would need a new box for every new number,', 'end': 54.261}
- t= 54.261s  cue_end       cue-017  {}
- t= 54.261s  cue_start     cue-018  {'text': 'and we would forget where the latest number lives.', 'end': 57.694}
- t= 57.694s  cue_end       cue-018  {}
- t= 57.694s  cue_start     cue-019  {'text': 'So we reassign.', 'end': 59.104}
- t= 59.100s  event_end     ev_arrow  {'motion_id': 'motion.util.create_line'}
- t= 59.104s  cue_end       cue-019  {}
- t= 59.104s  cue_start     cue-020  {'text': 'We write score equals ten.', 'end': 61.082}
- t= 59.150s  event_end     ev_value0  {'motion_id': 'motion.appearance.fade_in'}
- t= 59.150s  event_start   ev_replace  {'motion_id': 'motion.transform.replacement', 'end': 68.65, 'run_time': 1.25, 'play_end': 60.4, 'label': '0 becomes 10'}
- t= 61.082s  cue_end       cue-020  {}
- t= 61.082s  cue_start     cue-021  {'text': 'We are not creating a second box labeled score.', 'end': 64.515}
- t= 64.515s  cue_end       cue-021  {}
- t= 64.515s  cue_start     cue-022  {'text': 'We are opening the same box and replacing the note inside.', 'end': 68.675}
- t= 68.650s  event_end     ev_replace  {'motion_id': 'motion.transform.replacement'}
- t= 68.675s  cue_end       cue-022  {}
- t= 68.675s  cue_start     cue-023  {'text': 'The name stays.', 'end': 70.085}
- t= 68.700s  event_start   ev_pulse  {'motion_id': 'motion.emphasis.pulse', 'end': 71.7, 'run_time': 1.25, 'play_end': 69.95, 'label': 'Pulse new value'}
- t= 70.085s  cue_end       cue-023  {}
- t= 70.085s  cue_start     cue-024  {'text': 'The value can change.', 'end': 71.699}
- t= 71.699s  cue_end       cue-024  {}
- t= 71.699s  cue_start     cue-025  {'text': 'After the assignment, whenever the program asks for score, it receives ten,', 'end': 76.113}
- t= 71.700s  event_end     ev_pulse  {'motion_id': 'motion.emphasis.pulse'}
- t= 71.750s  event_start   ev_focus  {'motion_id': 'motion.emphasis.focus_set', 'end': 82.7, 'run_time': 1.35, 'play_end': 73.1, 'label': 'Focus the card'}
- t= 76.113s  cue_end       cue-025  {}
- t= 76.113s  cue_start     cue-026  {'text': 'not zero.', 'end': 77.523}
- t= 77.523s  cue_end       cue-026  {}
- t= 77.523s  cue_start     cue-027  {'text': 'The visual is helpful: a lid you can read, and contents you can swap.', 'end': 82.774}
- t= 82.700s  event_end     ev_focus  {'motion_id': 'motion.emphasis.focus_set'}
- t= 82.774s  cue_end       cue-027  {}
- t= 82.774s  cue_start     cue-028  {'text': 'It also has limits.', 'end': 84.388}
- t= 84.388s  cue_end       cue-028  {}
- t= 84.388s  cue_start     cue-029  {'text': 'Real memory is not a wooden crate.', 'end': 87.094}
- t= 87.094s  cue_end       cue-029  {}
- t= 87.094s  cue_start     cue-030  {'text': 'The computer stores bits at an address,', 'end': 89.689}
- t= 89.689s  cue_end       cue-030  {}
- t= 89.689s  cue_start     cue-031  {'text': 'and the name is a label your programming language keeps for you.', 'end': 94.213}
- t= 94.200s  event_end     ev_heading  {'motion_id': 'motion.appearance.write'}
- t= 94.213s  cue_end       cue-031  {}
- t= 94.213s  cue_start     cue-032  {'text': 'Remember this: a variable binds a stable name to a replaceable value,', 'end': 98.626}
- t= 94.250s  event_start   ev_recap  {'motion_id': 'motion.appearance.smooth_entrance', 'end': 104.4, 'run_time': 1.15, 'play_end': 95.4, 'label': 'Recap line'}
- t= 98.626s  cue_end       cue-032  {}
- t= 98.626s  cue_start     cue-033  {'text': 'so the rest of the program can talk about the thing without chasing a moving number.', 'end': 104.426}
- t=104.400s  event_end     ev_box  {'motion_id': 'motion.appearance.grow_from_center'}
- t=104.400s  event_end     ev_name  {'motion_id': 'motion.appearance.write'}
- t=104.400s  event_end     ev_recap  {'motion_id': 'motion.appearance.smooth_entrance'}
- t=104.426s  cue_end       cue-033  {}
- t=104.426s  cue_start     cue-034  {'text': 'That is how a variable stores a value.', 'end': 107.495}
- t=104.500s  event_start   ev_end  {'motion_id': 'motion.group.parallel', 'end': 107.995, 'run_time': 1.4, 'play_end': 105.9, 'label': 'Fade everything out'}
- t=107.495s  cue_end       cue-034  {}
- t=107.995s  event_end     ev_end  {'motion_id': 'motion.group.parallel'}

## Narration (source of truth)

Imagine you are tidying a desk. You do not throw every paper into one anonymous pile. You take a small box, write a name on the lid, and place a single note inside.

A variable works in that same spirit. It is a named place in the computer's memory, reserved so your program can find a piece of information again.

The name on the box is not the information. It is the handle. When we write the word score, we are pointing at a location, not at the number itself.

Inside the box is the value. That is the information the name currently holds. At the beginning, score holds zero, because we have not counted anything yet.

Now, here's the important part. Programs change. If we could not change what a box contains, we would need a new box for every new number, and we would forget where the latest number lives.

So we reassign. We write score equals ten. We are not creating a second box labeled score. We are opening the same box and replacing the note inside.

The name stays. The value can change. After the assignment, whenever the program asks for score, it receives ten, not zero.

The visual is helpful: a lid you can read, and contents you can swap. It also has limits. Real memory is not a wooden crate. The computer stores bits at an address, and the name is a label your programming language keeps for you.

Remember this: a variable binds a stable name to a replaceable value, so the rest of the program can talk about the thing without chasing a moving number.

That is how a variable stores a value.
