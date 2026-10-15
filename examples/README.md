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

The report writes SRT/VTT next to the examples. Those timestamps are
**estimates**. They are not aligned to a voice recording. Override cue
times in the JSON (`timing_status: manual`) after you record voiceover;
keep the same cue ids.
