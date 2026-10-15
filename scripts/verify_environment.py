"""Independent renderer/notebook probes. Nonzero exit means NOT render-ready.

No installation, shell mutation, notebook magic, or skipped-as-success behavior.
Run with the intended notebook interpreter from the repository root.
"""
from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
import platform
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def command(args):
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=45)
        return result.returncode == 0, (result.stdout + result.stderr).strip()[:4000]
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def collect():
    checks = []

    def probe(name, operation, *, required=True):
        try:
            detail = operation()
            checks.append(dict(name=name, required=required, ok=True, detail=str(detail)))
        except Exception as exc:
            checks.append(dict(name=name, required=required, ok=False,
                               detail=f"{type(exc).__name__}: {exc}"))

    def module_version(name, package=None):
        module = importlib.import_module(name)
        return f"{importlib.metadata.version(package or name)}; {getattr(module, '__file__', '')}"

    def cmd(name, args, required=True):
        ok, detail = command(args)
        checks.append(dict(name=name, required=required, ok=ok, detail=detail))

    def python_check():
        if sys.version_info < (3, 10):
            raise RuntimeError('Project requires Python >=3.10; reference stack is 3.11')
        return sys.version

    probe('python', python_check)
    for mod in ['manim', 'numpy', 'scipy', 'av', 'jsonschema', 'IPython',
                'ipykernel', 'nbformat', 'nbclient', 'pytest']:
        probe(mod, lambda mod=mod: module_version(mod, 'ipython' if mod == 'IPython' else mod))
    cmd('python -m manim --version', [sys.executable, '-m', 'manim', '--version'])
    manim_cli = shutil.which('manim')
    # PATH CLI is diagnostic only; python -m manim is authoritative for the kernel.
    cmd('PATH manim --version', [manim_cli, '--version'], required=False) if manim_cli else checks.append(
        dict(name='PATH manim --version', required=False, ok=False, detail='Not on PATH; use python -m manim'))

    def cairo_test():
        import cairo
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 32, 32)
        context = cairo.Context(surface)
        context.set_source_rgb(0.2, 0.5, 0.8)
        context.paint()
        surface.flush()
        assert surface.get_width() == 32
        return f"binding {importlib.metadata.version('pycairo')}; native {cairo.cairo_version_string()}; painted surface OK"

    def pango_test():
        import manimpango
        fonts = manimpango.list_fonts()
        if not fonts:
            raise RuntimeError('Pango found no fonts')
        return f"{importlib.metadata.version('manimpango')}; {len(fonts)} fonts; sample {fonts[:8]}"

    def text_test():
        from manim import Text
        text = Text('QUONITRON: name = value', font='DejaVu Sans', warn_missing_font=False)
        assert text.width > 0 and text.height > 0
        return f"Actual Pango Text geometry {text.width:.3f} x {text.height:.3f}"

    def project_test():
        import quonitron_manim
        from quonitron_manim.design.theme import get_theme
        return f"{quonitron_manim.__file__}; theme {get_theme().name}"

    def av_encoder_test():
        import av
        from fractions import Fraction
        codec = av.CodecContext.create('libx264', 'w')
        codec.width = codec.height = 16
        codec.pix_fmt = 'yuv420p'
        codec.time_base = Fraction(1, 15)
        codec.open()
        return 'PyAV libx264 encoder opened; this is not a Manim scene render'

    probe('PyAV H.264 encoder', av_encoder_test)
    probe('Cairo painted surface', cairo_test)
    probe('Pango font discovery', pango_test)
    probe('Manim Text creation', text_test)
    probe('quonitron_manim import/theme', project_test)
    ffmpeg = shutil.which('ffmpeg')
    cmd('FFmpeg CLI (repository tests/frame extraction)', [ffmpeg, '-version']) if ffmpeg else checks.append(
        dict(name='FFmpeg CLI (repository tests/frame extraction)', required=True, ok=False, detail='Not on PATH'))
    for executable in ['git', 'pkg-config', 'latex', 'dvisvgm', 'code', 'ffprobe']:
        path = shutil.which(executable)
        checks.append(dict(name=executable, required=False, ok=bool(path), detail=path or 'Not on PATH'))
    cmd('Jupyter kernelspecs', [sys.executable, '-m', 'jupyter', 'kernelspec', 'list', '--json'])
    ready = all(check['ok'] for check in checks if check['required'])
    return dict(os=platform.platform(), architecture=platform.machine(),
                python_executable=sys.executable, prefix=sys.prefix, base_prefix=sys.base_prefix,
                reference_stack='Python 3.11 / Manim CE 0.19.0 / NumPy 2.2.6',
                ready=ready, status='READY_FOR_RENDER_ATTEMPT' if ready else 'BLOCKED_NOT_RENDER_VERIFIED',
                checks=checks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    report = collect()
    print(f"{report['os']} / {report['architecture']}\nPython: {report['python_executable']}")
    for check in report['checks']:
        print(f"{'PASS' if check['ok'] else 'FAIL' if check['required'] else 'OPTIONAL MISSING'} "
              f"{check['name']}: {check['detail']}")
    print(report['status'])
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2), encoding='utf-8')
    return 0 if report['ready'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
