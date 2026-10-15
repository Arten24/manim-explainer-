"""Publish compact CI evidence via GitHub Checks API when artifact hosts are blocked.

Run only in Actions with explicit checks:write. Tokens are read from the process
and never printed or written. Videos/full logs remain normal Actions artifacts.
Checks carry actual frame images as base64 JSON, NOT a visual approval.
"""
from __future__ import annotations
import base64
import argparse
import io
import json
import os
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preliminary', action='store_true')
    parser.add_argument('--notebook-only', action='store_true')
    parser.add_argument('--tests-only', action='store_true')
    args = parser.parse_args()
    root = Path.cwd()
    repo = os.environ['GITHUB_REPOSITORY']
    sha = os.environ['GITHUB_SHA']
    token = os.environ['GITHUB_TOKEN']
    if os.environ.get('GITHUB_ACTIONS') != 'true':
        raise RuntimeError('Evidence publication is restricted to GitHub Actions')

    def publish(name, summary, text, conclusion='success'):
        body = dict(name=name, head_sha=sha, status='completed', conclusion=conclusion,
                    output=dict(title=name, summary=summary, text=text))
        request = urllib.request.Request(
            f'https://api.github.com/repos/{repo}/check-runs',
            data=json.dumps(body).encode(), method='POST',
            headers={'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json',
                     'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28'})
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.load(response)
        print(f'Published {name}: check {result["id"]}')

    if args.notebook_only:
        executed = root / 'media/environment-setup/environment_render_test.executed.ipynb'
        data = json.loads(executed.read_text()) if executed.exists() else {'cells': []}
        cells = [c for c in data['cells'] if c['cell_type'] == 'code']
        outputs = [o for c in cells for o in c.get('outputs', [])]
        errors = [{'name': o.get('ename'), 'message': o.get('evalue')} for o in outputs if o['output_type'] == 'error']
        videos = sum('<video' in ''.join(o.get('data', {}).get('text/html', [])) for o in outputs)
        report = dict(code_cells=len(cells), executed_cells=sum(c.get('execution_count') is not None for c in cells),
                      errors=errors, video_html_outputs=videos,
                      inline_browser_playback='NOT_VERIFIED', sha=sha)
        ok = bool(cells) and report['executed_cells'] == len(cells) and not errors and videos == 7
        publish('QUONITRON notebook evidence', 'Actual notebook backend; browser playback is not certified.',
                json.dumps(report, indent=2), 'success' if ok else 'failure')
        return

    if args.tests_only:
        tests = root / 'media/cloud-verification/tests.xml'
        suites = ET.parse(tests).getroot()
        import platform
        report = dict(sha=sha, platform=platform.platform(),
                      tests={k: sum(int(x.get(k, 0)) for x in suites.iter('testsuite'))
                             for k in ('tests', 'failures', 'errors', 'skipped')},
                      problems=[{'test': case.get('name'), 'message': (failure.text or '')[-5000:]}
                                for case in suites.iter('testcase') for failure in case
                                if failure.tag in ('failure', 'error')],
                      durations={case.get('name'): case.get('time') for case in suites.iter('testcase')})
        ok = not any(report['tests'][k] for k in ('failures', 'errors', 'skipped'))
        publish('QUONITRON render-test evidence', 'Actual JUnit counts and failures from the renderer test job.',
                json.dumps(report, indent=2), 'success' if ok else 'failure')
        return

    diagnostics = root / 'media/cloud-verification/dependencies.json'
    tests = root / 'media/cloud-verification/tests.xml'
    report = {'sha': sha, 'visual_review': 'NOT_PERFORMED_BY_CI', 'browser_playback': 'NOT_VERIFIED'}
    if diagnostics.exists(): report['dependencies'] = json.loads(diagnostics.read_text())
    if tests.exists():
        suites = ET.parse(tests).getroot()
        report['tests'] = {k: sum(int(s.get(k, 0)) for s in suites.iter('testsuite'))
                           for k in ('tests', 'failures', 'errors', 'skipped')}
        report['test_problems'] = [{'test': case.get('name'), 'message': failure.text[-5000:]}
                                   for case in suites.iter('testcase')
                                   for failure in list(case) if failure.tag in ('failure', 'error')]
    manifests = list((root / 'media/environment-verification').rglob('report.json'))
    renders = [result for manifest in manifests
               for result in json.loads(manifest.read_text())['results']]
    report['renders'] = renders
    for result in renders:
        if not result.get('rendered'):
            log = Path(result['log'])
            result['error_tail'] = log.read_text(errors='replace')[-5000:] if log.exists() else 'No log'
    notebook = root / 'media/cloud-verification/notebook.log'
    if notebook.exists(): report['notebook_tail'] = notebook.read_text(errors='replace')[-4000:]
    failed = (not report.get('dependencies', {}).get('ready') or not report.get('tests')
              or any(report.get('tests', {}).get(k, 0) for k in ('failures', 'errors', 'skipped'))
              or len(renders) < 7 or any(r['status'] != 'RENDERED_AND_DECODED_NOT_VISUALLY_REVIEWED' for r in renders))
    text = json.dumps(report, indent=2)
    if len(text) > 64000:
        raise RuntimeError('Evidence report exceeds Checks API limit; inspect artifact instead')
    publish('QUONITRON preliminary render evidence' if args.preliminary else 'QUONITRON cloud evidence',
            'Actual probes/renders; preliminary reports do NOT certify tests or notebook execution.',
            text, 'neutral' if args.preliminary else 'failure' if failed else 'success')
    from PIL import Image
    for index, result in enumerate(renders):
        valid = [f for f in result.get('frames', []) if f['ok']]
        if not valid: continue
        # One settled sample per scene plus mid-transition/context samples.
        chosen = [valid[0], valid[-1]] if len(valid) > 1 else valid
        if result['scene'] in ('CodeToMemoryJourney', 'AssignmentInType', 'LayoutRepairExercise'):
            chosen += valid[1:3]
        if result['scene'] == 'CodeToMemoryJourney':
            chosen += [f for f in valid if f['time'] in (49, 54)]
        for frame in chosen:
            image = Image.open(frame['path']).convert('RGB')
            source_width, source_height = image.size
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=85)
            if len(buffer.getvalue()) > 44000:
                image.thumbnail((854, 480))
                buffer = io.BytesIO(); image.save(buffer, format='JPEG', quality=65)
            payload = dict(scene=result['scene'], timestamp=frame['time'], width=image.width,
                           height=image.height, source_width=source_width, source_height=source_height, mime='image/jpeg',
                           data=base64.b64encode(buffer.getvalue()).decode())
            text = json.dumps(payload)
            if len(text) >= 64000:
                raise RuntimeError('Frame exceeds Checks API evidence limit; use artifact')
            publish(f'Frame {index}: {result["scene"]} {frame["time"]}s',
                    'Actual extracted video frame, JPEG encoded for API transport. Human review required.', text)


if __name__ == '__main__':
    main()
