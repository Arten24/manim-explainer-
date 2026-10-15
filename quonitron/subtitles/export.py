"""SRT and WebVTT export for estimated subtitle tracks."""

from __future__ import annotations

from pathlib import Path

from quonitron.subtitles.models import SubtitleCue, SubtitleTrack


def format_timestamp(seconds: float, *, vtt: bool = False) -> str:
    if seconds < 0:
        raise ValueError("Timestamp cannot be negative")
    millis = int(round(seconds * 1000.0))
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    sep = "." if vtt else ","
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{sep}{ms:03d}"


def _wrap_line(text: str, max_chars: int) -> str:
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


def to_srt(track: SubtitleTrack) -> str:
    blocks = []
    for index, cue in enumerate(track.cues, start=1):
        text = _wrap_line(cue.text, track.max_line_chars)
        blocks.append(
            f"{index}\n"
            f"{format_timestamp(cue.start_seconds)} --> "
            f"{format_timestamp(cue.end_seconds)}\n"
            f"{text}"
        )
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def to_vtt(track: SubtitleTrack) -> str:
    blocks = ["WEBVTT", f"NOTE {track.notes}"]
    for cue in track.cues:
        text = _wrap_line(cue.text, track.max_line_chars)
        ident = f"{cue.scene_id}-{cue.sequence}"
        blocks.append(
            f"{ident}\n"
            f"{format_timestamp(cue.start_seconds, vtt=True)} --> "
            f"{format_timestamp(cue.end_seconds, vtt=True)}\n"
            f"{text}"
        )
    return "\n\n".join(blocks) + "\n"


def write_srt(track: SubtitleTrack, path: Path) -> Path:
    path = Path(path)
    path.write_text(to_srt(track), encoding="utf-8")
    return path


def write_vtt(track: SubtitleTrack, path: Path) -> Path:
    path = Path(path)
    path.write_text(to_vtt(track), encoding="utf-8")
    return path


def estimate_duration(text: str, wpm: int, min_d: float, max_d: float) -> float:
    words = max(1, len(text.split()))
    seconds = (words / float(wpm)) * 60.0
    return max(min_d, min(max_d, seconds))


def cues_from_sentences(
    sentences: list[str],
    scene_id: str,
    *,
    reading_wpm: int = 160,
    min_duration: float = 1.2,
    max_duration: float = 6.0,
    start_at: float = 0.0,
) -> SubtitleTrack:
    """Build a track from complete sentences with estimated timings."""
    track = SubtitleTrack(
        reading_wpm=reading_wpm,
        min_duration=min_duration,
        max_duration=max_duration,
    )
    cursor = start_at
    seq = 1
    for raw in sentences:
        text = " ".join(raw.split())
        if not text:
            continue
        dur = estimate_duration(text, reading_wpm, min_duration, max_duration)
        track.add(
            SubtitleCue(
                scene_id=scene_id,
                sequence=seq,
                text=text,
                start_seconds=round(cursor, 3),
                end_seconds=round(cursor + dur, 3),
            )
        )
        cursor += dur
        seq += 1
    return track
