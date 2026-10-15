# Examples

## Part 1 — foundation demo

```bash
manim -ql examples/foundation_demo.py VariableStoresAValue
```

## Part 2 — motion + shared timeline

Narration source: `variable_narration.txt`  
Clock: `variable_timeline.json`  
Scene: `motion_timeline_demo.py`

```bash
python scripts/timeline_report.py
manim -ql examples/motion_timeline_demo.py VariableMemoryTimeline
```

## Part 3 — transitions + the same clock

Narration: `journey_narration.txt`  
Clock: `journey_timeline.json`  
Scene: `journey_demo.py`

```bash
python scripts/timeline_report.py examples/journey_timeline.json --out examples/journey_timeline_report.md
manim -ql examples/journey_demo.py CodeToMemoryJourney
```

Beats in the JSON are chapters. They do not start a second timer. `cue-008`
is written to continue across the code → memory change.

## Part 4 — typography

Narration: `text_narration.txt`  
Clock: `text_timeline.json`  
Scene: `text_typography_demo.py`  
Notebook: `notebooks/part04_text_typography_demo.ipynb`

```bash
python scripts/timeline_report.py examples/text_timeline.json --out examples/text_timeline_report.md
manim -ql examples/text_typography_demo.py AssignmentInType
```

The report writes SRT/VTT next to the examples. Those timestamps are
**estimates**. They are not aligned to a voice recording. Override cue
times in the JSON (`timing_status: manual`) after you record voiceover;
keep the same cue ids.
