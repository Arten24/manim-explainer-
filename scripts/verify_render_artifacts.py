#!/usr/bin/env python3
"""Check rendered MP4 metadata and extract a midpoint frame for inspection."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def inspect_video(video: Path, frames_dir: Path, index: int) -> dict[str, object]:
    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=codec_name,width,height,avg_frame_rate:format=duration,size",
            "-of",
            "json",
            str(video),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    details = json.loads(probe.stdout)
    streams = details.get("streams", [])
    if not streams:
        raise ValueError(f"No video stream found in {video}")
    stream = streams[0]
    fmt = details.get("format", {})
    duration = float(fmt.get("duration", 0))
    if duration <= 0 or int(stream.get("width", 0)) <= 0 or int(stream.get("height", 0)) <= 0:
        raise ValueError(f"Invalid video stream metadata for {video}: {details}")

    frames_dir.mkdir(parents=True, exist_ok=True)
    frame = frames_dir / f"{index:02d}_{video.stem}_mid.jpg"
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-ss",
            f"{duration / 2:.3f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(frame),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    if not frame.is_file() or frame.stat().st_size == 0:
        raise ValueError(f"Frame extraction produced no image for {video}")

    return {
        "video": str(video),
        "codec": stream.get("codec_name"),
        "size": f"{stream['width']}x{stream['height']}",
        "frame_rate": stream.get("avg_frame_rate"),
        "duration_seconds": round(duration, 3),
        "file_bytes": int(fmt.get("size", video.stat().st_size)),
        "midpoint_frame": str(frame),
        "frame_bytes": frame.stat().st_size,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media_dir", type=Path, help="Directory containing rendered MP4s")
    parser.add_argument("--frames-dir", type=Path, required=True)
    parser.add_argument("--min-videos", type=int, default=1)
    args = parser.parse_args()

    for executable in ("ffprobe", "ffmpeg"):
        if shutil.which(executable) is None:
            print(f"FAIL: {executable} is not available on PATH", file=sys.stderr)
            return 2

    videos = sorted(args.media_dir.rglob("*.mp4"))
    if len(videos) < args.min_videos:
        print(
            f"FAIL: found {len(videos)} MP4 file(s) under {args.media_dir}; "
            f"expected at least {args.min_videos}",
            file=sys.stderr,
        )
        return 1

    try:
        for index, video in enumerate(videos, start=1):
            report = inspect_video(video, args.frames_dir, index)
            print(
                "PASS: {video} — {codec}, {size}, {duration_seconds}s, "
                "frame {midpoint_frame}".format(**report)
            )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()
        print(
            f"FAIL: command exited {exc.returncode}: {exc.cmd}\n{detail}",
            file=sys.stderr,
        )
        return 1
    except (OSError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
