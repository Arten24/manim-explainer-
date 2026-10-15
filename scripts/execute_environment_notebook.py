"""Execute the setup notebook headlessly; errors/blocked renders fail the command.

This validates backend execution and generated HTML, NOT VS Code video playback.
The tracked notebook stays clean; executed output is saved under ignored media/.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    import nbformat
    from nbclient import NotebookClient

    notebook = nbformat.read(ROOT / 'notebooks/environment_render_test.ipynb', as_version=4)
    output = ROOT / 'media/environment-setup/environment_render_test.executed.ipynb'
    output.parent.mkdir(parents=True, exist_ok=True)
    code = 0
    try:
        NotebookClient(notebook, timeout=1800, kernel_name='python3',
                       resources={'metadata': {'path': str(ROOT)}}).execute()
    except Exception as exc:
        code = 1
        print(f'NOTEBOOK FAILED OR BLOCKED: {type(exc).__name__}: {exc}', file=sys.stderr)
    finally:
        nbformat.write(notebook, output)
        print('Executed/partially executed notebook:', output)
    if code == 0:
        print('Backend notebook execution succeeded; frontend playback NOT verified by this command.')
    return code


if __name__ == '__main__':
    raise SystemExit(main())
