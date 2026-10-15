"""SRT and WebVTT export for estimated subtitle tracks."""

from __future__ import annotations

import json
import math
import html
from pathlib import Path
from typing import Union

from quonitron_manim.subtitles.models import SubtitleTrack
from quonitron_manim.subtitles.validation import validate_track

PathLike = Union[str, Path]


def format_timestamp(seconds: float, *, vtt: bool = False) -> str:
    if not math.isfinite(seconds) or seconds < 0:
        raise ValueError("Timestamp must be finite and nonnegative")
    millis = int(round(seconds * 1000.0))
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    sep = "." if vtt else ","
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{sep}{ms:03d}"


def _wrap(text: str, max_chars: int) -> str:
    words = text.strip().split()
    if not words:
        return ""
    lines: list[str] = []
    current: list[str] = []
    length = 0
    for word in words:
        extra = len(word) + (1 if current else 0)
        if current and length + extra > max_chars:
            lines.append(" ".join(current))
            current = [word]
            length = len(word)
        else:
            current.append(word)
            length += extra
    if current:
        lines.append(" ".join(current))
    return "\n".join(lines)


def to_srt(track: SubtitleTrack, *, validate: bool = True) -> str:
    if validate:
        validate_track(track).raise_if_invalid()
    blocks = []
    for index, cue in enumerate(sorted(track.cues, key=lambda c: (c.start_time, c.sequence, c.id)), start=1):
        if int(round(cue.end_time * 1000)) <= int(round(cue.start_time * 1000)):
            raise ValueError(f"{cue.id}: cue collapses at millisecond export precision")
        body = html.escape(cue.text if track.preserve_lines else _wrap(cue.text, track.max_chars), quote=False)
        blocks.append(
            f"{index}\n"
            f"{format_timestamp(cue.start_time)} --> "
            f"{format_timestamp(cue.end_time)}\n"
            f"{body}"
        )
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def to_vtt(track: SubtitleTrack, *, validate: bool = True) -> str:
    if validate:
        validate_track(track).raise_if_invalid()
    note = " ".join(track.notes.split()).replace("-->", "→")
    blocks = ["WEBVTT"] + ([f"NOTE {note}"] if note else [])
    for cue in sorted(track.cues, key=lambda c: (c.start_time, c.sequence, c.id)):
        if int(round(cue.end_time * 1000)) <= int(round(cue.start_time * 1000)):
            raise ValueError(f"{cue.id}: cue collapses at millisecond export precision")
        ident = cue.id
        body = html.escape(cue.text if track.preserve_lines else _wrap(cue.text, track.max_chars), quote=False)
        blocks.append(
            f"{ident}\n"
            f"{format_timestamp(cue.start_time, vtt=True)} --> "
            f"{format_timestamp(cue.end_time, vtt=True)}\n"
            f"{body}"
        )
    return "\n\n".join(blocks) + "\n"


def write_srt(track: SubtitleTrack, path: PathLike) -> Path:
    path = Path(path)
    path.write_text(to_srt(track), encoding="utf-8")
    return path


def write_vtt(track: SubtitleTrack, path: PathLike) -> Path:
    path = Path(path)
    path.write_text(to_vtt(track), encoding="utf-8")
    return path


def load_track(path: PathLike) -> SubtitleTrack:
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if "cues" not in data:
        raise ValueError(f"{path} is not a subtitle track JSON file")
    return SubtitleTrack.from_dict(data)


def estimate_duration(text: str, wpm: int, min_d: float, max_d: float) -> float:
    words = max(1, len(text.split()))
    seconds = (words / float(wpm)) * 60.0
    return max(min_d, min(max_d, seconds))
