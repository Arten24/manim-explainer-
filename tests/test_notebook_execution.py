from pathlib import Path

import pytest

nbformat = pytest.importorskip("nbformat")
nbclient = pytest.importorskip("nbclient")


def test_part4_notebook_executes_without_renderer(repo_root: Path):
    notebook_path = repo_root / "notebooks" / "part04_text_typography_demo.ipynb"
    notebook = nbformat.read(notebook_path, as_version=4)
    nbformat.validate(notebook)

    client = nbclient.NotebookClient(
        notebook,
        timeout=120,
        kernel_name="python3",
        resources={"metadata": {"path": str(repo_root)}},
    )
    executed = client.execute()
    code_cells = [cell for cell in executed.cells if cell.cell_type == "code"]

    assert code_cells
    assert all(cell.execution_count is not None for cell in code_cells)
    assert any(
        output.output_type == "stream" and "timeline assignment_type" in output.text
        for cell in code_cells
        for output in cell.get("outputs", [])
    )
