"""Fetch API-readable verification JSON/frames without following artifact URLs.

Read-only GitHub operation. Uses existing gh authentication; never reads tokens.
    python scripts/fetch_ci_evidence.py --sha <verified-commit>
"""
import argparse
import base64
import json
from pathlib import Path
import re
import subprocess


def gh_json(*args):
    return json.loads(subprocess.check_output(['gh', *args], text=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sha', required=True)
    parser.add_argument('--output', type=Path, default=Path('media/cloud-verification/github'))
    args = parser.parse_args()
    if not re.fullmatch('[0-9a-f]{40}', args.sha):
        parser.error('Use a full verified commit SHA')
    repo = gh_json('repo', 'view', '--json', 'nameWithOwner')['nameWithOwner']
    checks = gh_json('api', f'repos/{repo}/commits/{args.sha}/check-runs?per_page=100')['check_runs']
    dest = args.output / args.sha
    dest.mkdir(parents=True, exist_ok=True)
    saved = []
    for check in checks:
        text = check.get('output', {}).get('text')
        if check['name'] in ('QUONITRON cloud evidence', 'QUONITRON preliminary render evidence') and text:
            report = json.loads(text)
            path = dest / f'report-{check["id"]}.json'
            path.write_text(json.dumps(report, indent=2), encoding='utf-8')
            saved.append(str(path))
        elif check['name'].startswith('Frame ') and text:
            frame = json.loads(text)
            if frame['mime'] != 'image/jpeg':
                raise ValueError('Unexpected frame format')
            safe_name = re.sub('[^a-zA-Z0-9_.-]', '_', frame['scene'])
            path = dest / f'{safe_name}-{frame["timestamp"]}-{check["id"]}.jpg'
            path.write_bytes(base64.b64decode(frame['data'], validate=True))
            saved.append(str(path))
    print(json.dumps({'repo': repo, 'sha': args.sha, 'saved': saved}, indent=2))
    if not saved:
        print('No published evidence yet; not a rendering success.')
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
