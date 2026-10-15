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


def test_probe_records_useful_metadata(tmp_path, monkeypatch):
    module = load_script('verify_renders')
    movie = tmp_path / 'sample.mp4'
    movie.write_bytes(b'metadata-unit-test-not-a-real-render')
    payload = {'streams': [{'codec_name': 'h264', 'width': 1920, 'height': 1080,
                            'avg_frame_rate': '30000/1001'}],
               'format': {'duration': '1.5', 'size': str(movie.stat().st_size)}}
    def fake_probe(args, log, **kwargs):
        assert args[0] == '/test/ffprobe' and kwargs['timeout'] == 30
        log.write_text(json.dumps(payload))
        return 0
    monkeypatch.setattr(module.shutil, 'which', lambda _: '/test/ffprobe')
    monkeypatch.setattr(module, 'execute', fake_probe)
    metadata = module.probe_movie(movie, tmp_path / 'probe.json')
    assert metadata == dict(codec='h264', width=1920, height=1080,
                            frame_rate='30000/1001', duration_seconds=1.5,
                            file_bytes=movie.stat().st_size)


@pytest.mark.parametrize('payload', [
    {}, {'streams': []},
    {'streams': [{'width': 0, 'height': 480, 'avg_frame_rate': '15', 'codec_name': 'h264'}],
     'format': {'duration': '1'}},
    {'streams': [{'width': 854, 'height': 480, 'avg_frame_rate': '0/0', 'codec_name': 'h264'}],
     'format': {'duration': '1'}},
    {'streams': [{'width': 854, 'height': 480, 'avg_frame_rate': '15', 'codec_name': 'h264'}],
     'format': {'duration': 'nan'}},
])
def test_invalid_probe_metadata_is_rejected(tmp_path, monkeypatch, payload):
    module = load_script('verify_renders')
    monkeypatch.setattr(module.shutil, 'which', lambda _: '/test/ffprobe')
    def fake_probe(args, log, **kwargs):
        log.write_text(json.dumps(payload))
        return 0
    monkeypatch.setattr(module, 'execute', fake_probe)
    with pytest.raises(ValueError, match='Invalid ffprobe metadata'):
        module.probe_movie(tmp_path / 'unused.mp4', tmp_path / 'probe.json')


def test_probe_command_failure_and_missing_executable(tmp_path, monkeypatch):
    module = load_script('verify_renders')
    monkeypatch.setattr(module.shutil, 'which', lambda _: None)
    with pytest.raises(ValueError, match='unavailable'):
        module.probe_movie(tmp_path / 'unused.mp4', tmp_path / 'probe.json')
    monkeypatch.setattr(module.shutil, 'which', lambda _: '/test/ffprobe')
    monkeypatch.setattr(module, 'execute', lambda *a, **kw: 9)
    with pytest.raises(ValueError, match='exit 9'):
        module.probe_movie(tmp_path / 'unused.mp4', tmp_path / 'probe.json')


def test_probe_failure_cannot_be_counted_as_decoded(tmp_path, monkeypatch):
    module = load_script('verify_renders')
    def fake_render(args, *a, **kw):
        destination = Path(args[args.index('--media_dir') + 1])
        (destination / 'MinimalRenderCheck.mp4').write_bytes(b'not-a-real-render')
        return 0
    def reject_probe(*a, **kw):
        raise ValueError('invalid stream')
    monkeypatch.setattr(module, 'execute', fake_render)
    monkeypatch.setattr(module.shutil, 'which', lambda _: '/test/ffmpeg')
    monkeypatch.setattr(module, 'probe_movie', reject_probe)
    result = module.render_case('minimal', tmp_path)
    assert result['rendered'] and not result['decoded']
    assert result['status'] == 'RENDERED_BUT_PROBE_FAILED'
