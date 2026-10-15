# Examples

## Foundation demo

Explains how a variable stores a value using the Part 1 design system,
`TitleCard`, `SectionHeading`, and `VariableStore`.

```bash
# from the repository root
pip install -e ".[dev]"
manim -ql examples/foundation_demo.py VariableStoresAValue
```

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
manim -ql examples/foundation_demo.py VariableStoresAValue
```

Low-quality (`-ql`) is 480p15 and is the intended smoke render. Do not use
`-qh` for routine checks.

On-screen captions come from `subtitle_demo.json`. Export the same cues to
files without rendering:

```bash
python -c "from pathlib import Path; from quonitron_manim.subtitles import load_track, write_srt, write_vtt; t=load_track('examples/subtitle_demo.json'); write_srt(t, Path('examples/subtitle_demo.srt')); write_vtt(t, Path('examples/subtitle_demo.vtt'))"
```

Those timestamps are **estimates**. They are not aligned to a voice recording.
