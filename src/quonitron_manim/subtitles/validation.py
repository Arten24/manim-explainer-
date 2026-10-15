"""Validate subtitle tracks without touching video or audio files."""

from __future__ import annotations

import math

from dataclasses import dataclass, field
from typing import List

from quonitron_manim.subtitles.models import SubtitleCue, SubtitleTrack

ALLOWED_OVERLAP_POLICIES = frozenset({"error", "warn", "allow"})


@dataclass
class SubtitleIssue:
    level: str
    message: str
    cue_id: str | None = None


@dataclass
class ValidationReport:
    issues: List[SubtitleIssue] = field(default_factory=list)

    @property
    def errors(self) -> List[SubtitleIssue]:
        return [item for item in self.issues if item.level == "error"]

    @property
    def warnings(self) -> List[SubtitleIssue]:
        return [item for item in self.issues if item.level == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def raise_if_invalid(self) -> None:
        if self.errors:
            joined = "; ".join(item.message for item in self.errors)
            raise ValueError(joined)


def _check_cue(cue: SubtitleCue, track: SubtitleTrack, report: ValidationReport) -> None:
    text = cue.text.strip()
    if len(text) > track.max_chars:
        report.issues.append(
            SubtitleIssue(
                "warning",
                f"{cue.id}: {len(text)} characters exceeds max_chars={track.max_chars}",
                cue.id,
            )
        )
    if cue.duration + 1e-9 < track.min_duration:
        report.issues.append(
            SubtitleIssue(
                "warning",
                f"{cue.id}: duration {cue.duration:.3f}s is under min_duration="
                f"{track.min_duration}",
                cue.id,
            )
        )
    if cue.duration - 1e-9 > track.max_duration:
        report.issues.append(
            SubtitleIssue(
                "warning",
                f"{cue.id}: duration {cue.duration:.3f}s exceeds max_duration="
                f"{track.max_duration}",
                cue.id,
            )
        )


def validate_track(track: SubtitleTrack) -> ValidationReport:
    report = ValidationReport()
    if track.overlap_policy not in ALLOWED_OVERLAP_POLICIES:
        report.issues.append(
            SubtitleIssue(
                "error",
                f"Unknown overlap_policy {track.overlap_policy!r}. "
                f"Use one of {sorted(ALLOWED_OVERLAP_POLICIES)}",
            )
        )
        return report

    if (not math.isfinite(track.min_duration) or not math.isfinite(track.max_duration)
            or track.min_duration <= 0 or track.max_duration < track.min_duration
            or track.reading_wpm <= 0 or track.max_chars < 1):
        report.issues.append(SubtitleIssue("error", "Invalid track duration/reading/width settings"))
    seen_ids = set()
    ordered = sorted(track.cues, key=lambda c: (c.start_time, c.sequence))
    for cue in ordered:
        if cue.id in seen_ids:
            report.issues.append(
                SubtitleIssue("error", f"Duplicate cue id {cue.id!r}", cue.id)
            )
        seen_ids.add(cue.id)
        try:
            cue.__post_init__()
        except (ValueError, TypeError) as exc:
            report.issues.append(SubtitleIssue("error", str(exc), cue.id))
        _check_cue(cue, track, report)

    for index, left in enumerate(ordered):
        for right in ordered[index + 1:]:
            if right.start_time >= left.end_time - 1e-9:
                break
            message = f"Cues {left.id} and {right.id} overlap ({left.end_time:.3f} > {right.start_time:.3f})"
            if track.overlap_policy != "allow":
                report.issues.append(SubtitleIssue("error" if track.overlap_policy == "error" else "warning", message, right.id))

    sequences = [cue.sequence for cue in track.cues]
    if sequences != sorted(sequences):
        report.issues.append(
            SubtitleIssue("warning", "Cue sequence numbers are not sorted")
        )
    return report
