"""Execute Part 5 notebook backend; --strict requires its actual rendered preview."""
from pathlib import Path
import argparse
import os
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    import nbformat
    from nbclient import NotebookClient
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    notebook = nbformat.read(ROOT / "notebooks/part05_subtitle_sync.ipynb", as_version=4)
    output = ROOT / "media/part5/part05_subtitle_sync.executed.ipynb"
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.strict:
        os.environ["QUONITRON_REQUIRE_RENDER"] = "1"
    result = 0
    try:
        NotebookClient(notebook, timeout=600, kernel_name="python3",
                       resources={"metadata": {"path": str(ROOT)}}).execute()
    except Exception as exc:
        print(f"NOTEBOOK FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        result = 1
    finally:
        nbformat.write(notebook, output)
    outputs = [o for c in notebook.cells for o in c.get("outputs", [])]
    html = sum("text/html" in o.get("data", {}) for o in outputs)
    errors = sum(o.output_type == "error" for o in outputs)
    skips = sum("RENDER SKIPPED:" in o.get("text", "") for o in outputs)
    executed = sum(c.cell_type == "code" and c.execution_count is not None for c in notebook.cells)
    print(f"Executed {executed} code cells; errors={errors}; render skips={skips}; HTML outputs={html}")
    print(f"Backend only, frontend playback not certified. Output: {output}")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
