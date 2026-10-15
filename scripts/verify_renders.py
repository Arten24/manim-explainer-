"""Actual render + complete FFmpeg decode + frame extraction, with JSON evidence.

Run all: python scripts/verify_renders.py
Smoke:   python scripts/verify_renders.py --only minimal themed
1080p30: python scripts/verify_renders.py --only themed --quality production
A failed or unavailable renderer is a FAILURE, never a successful skip.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from fractions import Fraction
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    'subtitles': ('subtitle_sync_demo.py', 'SubtitleSyncDemo', [1, 3.7, 4.5, 7.5, 10.7]),
    'minimal': ('environment_smoke.py', 'MinimalRenderCheck', [0.4, 1.2]),
    'themed': ('environment_smoke.py', 'ThemeSubtitleRenderCheck', [0.4, 1.5]),
    'foundation': ('foundation_demo.py', 'VariableStoresAValue', [1, 5, 12, 20]),
    'motion': ('motion_timeline_demo.py', 'VariableMemoryTimeline', [5, 34, 59.4, 60, 95]),
    'transitions': ('journey_demo.py', 'CodeToMemoryJourney', [10, 22.8, 41, 49, 54, 65]),
    'typography': ('text_typography_demo.py', 'AssignmentInType', [3, 9, 28, 32, 38.3, 43.5, 47.6, 53]),
    'overlap': ('layout_audit_demo.py', 'LayoutRepairExercise', [1, 3.1, 3.6, 5]),
}


def execute(args, log, *, timeout=900, cwd=ROOT):
    """Preserve real errors including timeouts and missing executables."""
    log.parent.mkdir(parents=True, exist_ok=True)
    try:
        env = os.environ.copy()
        result = subprocess.run(args, cwd=cwd, env=env, capture_output=True,
                                text=True, timeout=timeout)
        text = result.stdout + result.stderr
        code = result.returncode
    except Exception as exc:
        code, text = -1, f'{type(exc).__name__}: {exc}'
    log.write_text(text, encoding='utf-8')
    return code


def probe_movie(movie, log):
    """Validate stream metadata in the existing verifier, not a second pipeline.

    Inspired by adb921d's inspect_video; retain timeout/error logs and full decode.
    A successful probe is metadata evidence only, never a successful render itself.
    """
    ffprobe = shutil.which('ffprobe')
    if not ffprobe:
        raise ValueError('ffprobe is unavailable')
    code = execute([ffprobe, '-v', 'error', '-select_streams', 'v:0',
                    '-show_entries', 'stream=codec_name,width,height,avg_frame_rate:format=duration,size',
                    '-of', 'json', str(movie)], log, timeout=30)
    if code != 0:
        raise ValueError(f'ffprobe failed with exit {code}; see {log}')
    try:
        data = json.loads(log.read_text(encoding='utf-8'))
        stream = data['streams'][0]
        duration = float(data['format']['duration'])
        width, height = int(stream['width']), int(stream['height'])
        rate = Fraction(stream['avg_frame_rate'])
        codec = stream['codec_name']
        if not math.isfinite(duration) or duration <= 0 or min(width, height) <= 0 or rate <= 0 or not codec:
            raise ValueError('Nonpositive/nonfinite stream metadata')
    except (ValueError, KeyError, IndexError, TypeError, ZeroDivisionError) as exc:
        raise ValueError(f'Invalid ffprobe metadata: {exc}') from exc
    return dict(codec=codec, width=width, height=height, frame_rate=str(rate),
                duration_seconds=duration, file_bytes=movie.stat().st_size)


def render_case(key, output, *, quality='low'):
    filename, scene, timestamps = CASES[key]
    destination = output / key
    destination.mkdir(parents=True, exist_ok=True)
    quality_args = ['-ql'] if quality == 'low' else ['-r', '1920,1080', '--fps', '30']
    args = [sys.executable, '-m', 'manim', *quality_args, '--renderer', 'cairo',
            '--format', 'mp4', '--disable_caching', '--media_dir', str(destination),
            str(ROOT / 'examples' / filename), scene]
    result = dict(scene=scene, command=args, rendered=False, decoded=False, frames=[],
                  status='RENDER_FAILED', log=str(destination / 'render.log'))
    result['exit_code'] = execute(args, destination / 'render.log')
    if result['exit_code'] != 0:
        return result
    movies = [p for p in destination.rglob(scene + '.mp4') if 'partial_movie_files' not in p.parts]
    movies = [p for p in movies if p.stat().st_size > 0]
    if not movies:
        result['status'] = 'FAILED_NO_NONEMPTY_MOVIE'
        return result
    movie = max(movies, key=lambda p: p.stat().st_mtime)
    result.update(rendered=True, movie=str(movie), bytes=movie.stat().st_size)
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg:
        result['status'] = 'RENDERED_BUT_FFMPEG_INSPECTION_BLOCKED'
        return result
    try:
        result['metadata'] = probe_movie(movie, destination / 'probe.json')
    except ValueError as exc:
        result.update(status='RENDERED_BUT_PROBE_FAILED', probe_error=str(exc))
        return result
    code = execute([ffmpeg, '-v', 'error', '-xerror', '-i', str(movie), '-f', 'null', '-'],
                   destination / 'decode.log')
    if code != 0:
        result['status'] = 'RENDERED_BUT_DECODE_FAILED'
        return result
    result['decoded'] = True
    for timestamp in timestamps:
        frame = destination / 'frames' / f'{timestamp:06.2f}.png'
        code = execute([ffmpeg, '-y', '-v', 'error', '-ss', str(timestamp), '-i', str(movie),
                        '-frames:v', '1', str(frame)], destination / 'frames' / f'{timestamp:06.2f}.log')
        exists = frame.is_file() and frame.stat().st_size > 0
        result['frames'].append(dict(time=timestamp, path=str(frame), ok=code == 0 and exists))
    result['status'] = ('RENDERED_AND_DECODED_NOT_VISUALLY_REVIEWED'
                        if all(f['ok'] for f in result['frames']) else 'FRAME_EXTRACTION_FAILED')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', nargs='+', choices=CASES, default=list(CASES))
    parser.add_argument('--quality', choices=['low', 'production'], default='low')
    parser.add_argument('--output', type=Path, default=ROOT / 'media' / 'environment-verification')
    args = parser.parse_args()
    # Unique directory prevents stale output from masquerading as this run's success.
    run = args.output.resolve() / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    results = []
    for key in args.only:
        result = render_case(key, run, quality=args.quality)
        results.append(result)
        print(f"{result['scene']}: {result['status']} (log: {result['log']})", flush=True)
    report = dict(python=sys.executable, quality=args.quality, results=results,
                  visual_review='NOT_PERFORMED_BY_SCRIPT', browser_playback='NOT_VERIFIED')
    run.mkdir(parents=True, exist_ok=True)
    (run / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('Evidence:', run / 'report.json')
    return 0 if all(r['status'] == 'RENDERED_AND_DECODED_NOT_VISUALLY_REVIEWED' for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
