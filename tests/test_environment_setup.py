"""Setup-tool regressions. No fake render is counted as a render test."""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_missing_command_captures_real_error(tmp_path):
    module = load_script('verify_renders')
    log = tmp_path / 'missing.log'
    assert module.execute(['quonitron-nonexistent-test-executable'], log) != 0
    assert 'FileNotFoundError' in log.read_text()


def test_success_exit_without_movie_is_failure(tmp_path, monkeypatch):
    module = load_script('verify_renders')
    monkeypatch.setattr(module, 'execute', lambda *a, **k: 0)
    result = module.render_case('minimal', tmp_path)
    assert result['status'] == 'FAILED_NO_NONEMPTY_MOVIE'
    assert not result['rendered']


def test_nonempty_movie_without_inspector_is_not_verified(tmp_path, monkeypatch):
    module = load_script('verify_renders')
    def render_stub(args, *a, **k):
        destination = Path(args[args.index('--media_dir') + 1])
        (destination / 'MinimalRenderCheck.mp4').write_bytes(b'not-a-real-movie')
        return 0
    monkeypatch.setattr(module, 'execute', render_stub)
    monkeypatch.setattr(module.shutil, 'which', lambda _: None)
    result = module.render_case('minimal', tmp_path)
    assert result['status'] == 'RENDERED_BUT_FFMPEG_INSPECTION_BLOCKED'
    assert not result['decoded']


def test_production_quality_matches_repo_1080p30(tmp_path, monkeypatch):
    module = load_script('verify_renders')
    monkeypatch.setattr(module, 'execute', lambda *a, **k: 1)
    command = module.render_case('themed', tmp_path, quality='production')['command']
    assert command[command.index('-r') + 1] == '1920,1080'
    assert command[command.index('--fps') + 1] == '30'


def test_setup_notebook_is_render_strict_and_uses_kernel_python():
    notebook = json.loads((ROOT / 'notebooks/environment_render_test.ipynb').read_text())
    text = '\n'.join(''.join(cell['source']) for cell in notebook['cells'])
    assert 'sys.executable' in text
    assert 'raise RuntimeError' in text
    assert 'embed=True' in text
    assert '%%manim' not in '\n'.join(''.join(c['source']) for c in notebook['cells'] if c['cell_type'] == 'code')
    assert not any(c.get('outputs') for c in notebook['cells'])


def test_reference_versions_agree():
    requirements = (ROOT / 'requirements-render.txt').read_text()
    environment = (ROOT / 'environment.windows.yml').read_text()
    assert 'manim==0.19.0' in requirements and 'manim=0.19.0' in environment
    assert 'numpy==2.2.6' in requirements and 'numpy=2.2.6' in environment


@pytest.mark.render
def test_real_environment_smoke_movies(tmp_path):
    """Actual Manim render/decode/frame checks, never the stubs above."""
    from quonitron_manim.core.manim_compat import manim_available, manimpango_usable
    import shutil
    if not manim_available() or not manimpango_usable()[0] or not shutil.which('ffmpeg'):
        pytest.skip('Real Cairo/Pango/Manim/FFmpeg stack unavailable; smoke movies NOT rendered')
    module = load_script('verify_renders')
    for key in ('minimal', 'themed'):
        result = module.render_case(key, tmp_path)
        assert result['status'] == 'RENDERED_AND_DECODED_NOT_VISUALLY_REVIEWED', result


def test_execute_creates_frame_directory_before_running(tmp_path):
    import sys
    module = load_script('verify_renders')
    target = tmp_path / 'frames' / 'frame.txt'
    log = target.with_suffix('.log')
    code = module.execute([sys.executable, '-c',
                           'from pathlib import Path; import sys; Path(sys.argv[1]).write_text("ok")',
                           str(target)], log)
    assert code == 0
    assert target.read_text() == 'ok'
