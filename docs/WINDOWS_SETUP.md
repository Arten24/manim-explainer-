# Windows + VS Code + Jupyter: dedicated rendering environment

Scope: environment setup and verification of existing Parts 1–4. No new library
features or Part 5. **The authoring sandbox is Debian Linux, not your Windows PC.**
The Windows solver, PowerShell script and VS Code playback have not been executed
on your PC. See [actual verification results](CLOUD_CAPABILITIES.md).

## 1. Chosen stack and alternatives

Reference target: **Windows 10/11 x86-64, Python 3.11, Manim Community 0.19.0,
NumPy 2.2.6, SciPy 1.15.3, PyAV 13.1.0, Cairo renderer**. This is not ManimGL.
The library's broader `>=0.18.1,<1.0` range is retained, not treated as proof that
all versions work. Requirements were checked against 0.19.0's published metadata
and its Conda-forge recipe, not guessed from the previous installation failure.

**Chosen: a separate Miniforge/Conda-forge environment.** It supplies compatible
compiled Cairo/Pango/PyAV/FFmpeg packages without a Windows compiler or pkg-config.
Use Conda for dependencies and pip **only for the editable local project** with
`--no-deps --no-build-isolation`. Do not install `requirements-render.txt` over it.

Alternatives evaluated:

- Windows pip/uv: 64-bit CPython wheels exist for relevant native packages, but
  selecting a version without a matching wheel causes native compilation/DLL
  problems. Viable for experienced users; not mixed into this setup.
- WSL2: reliable Debian/Ubuntu apt + pip native dependencies; adds Linux filesystem,
  WSL setup, and VS Code Remote-WSL/kernel selection. Good fallback, not a repair
  to your existing Windows environment. Keep its environment separate.
- Dev Container: repository configuration installs native packages and the pinned
  Python reference packages. Requires Docker and access to OS package registries.

### What is actually required?

| Dependency | Why / installation source |
|---|---|
| Python 3.11 | Dedicated reference interpreter; Conda-managed |
| Manim CE 0.19.0 | Existing Scene/Mobject/animation APIs; Conda-managed |
| NumPy 2.2.6 / SciPy 1.15.3 | Manim 0.19 requires NumPy >=2.1 on Python >=3.10, SciPy >=1.13; do not force NumPy 1.x |
| PyAV 13.1.0 | Manim 0.19 encodes video through PyAV (requires av >=9,<14) |
| pycairo + native Cairo | Cairo paths and surfaces; use Conda's binaries |
| manimpango + native Pango + fonts | All existing Text components; includes font discovery; Conda binaries/fonts |
| FFmpeg executable | **Not mandatory for Manim 0.19 encoding itself**; required by existing repository render tests, decode and frame-extraction commands |
| IPython/ipykernel | VS Code kernel and embedded Video output; pinned in the environment |
| nbclient/nbformat | Automated notebook validation/execution; pinned |
| jsonschema/pytest | Catalog/schema validation and tests; pinned |
| Git | Clone/update project; optional at render runtime |
| VS Code Python + Jupyter extensions | Windows frontend; not a Python package dependency |
| LaTeX + dvisvgm | Optional for actual MathTex; EquationText already catches TeX failures and falls back to Text |
| pkg-config / C compiler / Python development headers | Needed for Linux pip native source builds; **not required by this prebuilt Windows Conda route** |
| OpenGL GPU / audio / JupyterLab server | Not required for these Cairo scene/notebook previews |

`environment.windows.yml` pins principal Python packages and bounds native
packages; it is a **compatible environment specification**, not an exact
transitive, build-hashed lock. A Windows solve is still required. Export the
resolved platform lock after successful verification (section 8).

## 2. Install prerequisites on YOUR Windows PC

1. Install **Miniforge3 Windows x86-64**, Just Me, from its official releases:
   <https://github.com/conda-forge/miniforge/releases>. Choose
   `Miniforge3-Windows-x86_64.exe`; compare its SHA-256 with the release checksum
   (`Get-FileHash .\Miniforge3-Windows-x86_64.exe -Algorithm SHA256`). Do not use
   an unofficial DLL bundle. No global Python/PATH replacement is necessary.
2. Install Git for Windows if needed: <https://git-scm.com/download/win>.
3. Install VS Code and the Microsoft **Python** (`ms-python.python`) and
   **Jupyter** (`ms-toolsai.jupyter`) extensions.
4. Open **Miniforge Prompt** from Start. Launch `powershell` from that prompt;
   it inherits Conda's executable PATH. This avoids needing a permanent profile
   change. If `conda --version` is not found, reopen the Miniforge prompt rather
   than adding arbitrary Python directories to PATH.
5. Open the existing project checkout. The following path is an **example to
   replace**, not a library setting:

```powershell
Set-Location 'C:\Projects\manim-explainer-'
git --version
conda --version
```

No need to delete `.venv` or change an unrelated Python install. Use one route
below, not both. Internet access to Conda-forge and PyPI is required locally.

## 3. Automated NEW-environment setup

From the Miniforge-enabled PowerShell in the project:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup_windows.ps1
```

The execution-policy override applies only to that child process; it does not
permanently weaken the machine policy. Inspect the script first. Organization
policy may forbid this; use the manual commands below instead.

The script:

- Refuses to touch an existing `quonitron-manim-render` environment.
- Creates the environment from `environment.windows.yml`.
- Installs only this repository editable, without resolving pip dependencies.
- Refuses to overwrite a same-name user kernelspec.
- Registers a QUONITRON kernel, independently verifies dependencies, and renders
  minimal/themed smoke scenes with FFmpeg decoding and frame extraction.
- Returns an error on a failed solve, dependency probe, or render; does not print
  successful setup after a blocked render.

Choose a fresh name if one already exists:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup_windows.ps1 -Name quonitron-manim-render-v2
```

If a prior setup partially created an environment, the script leaves it intact.
Do not blindly delete it; inspect it or select a fresh name. If a kernelspec name
collides, use a distinct kernel name when registering manually.

## 4. Equivalent manual setup (use INSTEAD of section 3)

Check first; if the name already exists, **stop and inspect it**, or use a new name
consistently in every command. These commands are intended for a fresh name:

```powershell
conda env list
conda env create --file .\environment.windows.yml
# Check $LASTEXITCODE after each command; stop if nonzero.
conda run --no-capture-output -n quonitron-manim-render python -m pip install --no-deps --no-build-isolation -e .
conda run -n quonitron-manim-render jupyter kernelspec list
# Register only if this kernelspec name is not already in use:
conda run -n quonitron-manim-render python -m ipykernel install --user --name quonitron-manim-render --display-name 'QUONITRON Manim (quonitron-manim-render)'
conda run --no-capture-output -n quonitron-manim-render python scripts/verify_environment.py --json media/environment-setup/windows-diagnostics.json
conda run --no-capture-output -n quonitron-manim-render python scripts/verify_renders.py --only minimal themed
```

For an existing valid dedicated environment, skip creation and installation and
run verification first. The verifier prints individual real import/functionality
errors. Do not replace a working environment just to match the suggested name.

## 5. Select VS Code interpreter AND notebook kernel

From Miniforge Prompt, after setup:

```text
conda activate quonitron-manim-render
code .
```

If `code` is unavailable, launch VS Code normally and open the project folder;
the registered kernel should still be available. If Conda DLL discovery fails,
launch from the activated prompt using VS Code's installed executable or enable
its `code` CLI, rather than copying DLLs manually.

In VS Code:

1. **Python: Select Interpreter** → the Conda `quonitron-manim-render` interpreter.
2. Open `notebooks/environment_render_test.ipynb`.
3. Top right **Select Kernel** → **Jupyter Kernel** → registered QUONITRON kernel,
   or **Python Environments** → the same Conda environment. These are alternatives,
   not two simultaneous kernels. Selecting the editor interpreter alone is not
   sufficient for an already-open notebook.
4. Run diagnostics. `sys.executable` must point into the dedicated environment.
   Missing dependencies raise `BLOCKED`; do not call that successful rendering.
5. Run the helper cell, minimal scene, themed subtitle scene, overlap exercise,
   then existing Parts 1–4. Rendering uses `sys.executable -m manim`, not an
   unverified `%%manim` extension.
6. Play each embedded MP4, inspect PNG frames and check subtitles/transitions.
   Embedded HTML generation is not proof that the frontend played it.
7. Edit/save a scene `.py` file and rerun its cell. Each subprocess reloads code;
   each run gets a unique output directory. After changing dependencies, restart
   the kernel and rerun diagnostics.
8. If playback is unsupported, open the printed `.mp4` in a local video player.
   Check notebook trust and VS Code output/security settings before changing
   packages. Errors and output remain under ignored `media/`.

## 6. Full verification commands

Run from the repository root; these use the correct interpreter without assuming
an activated terminal. Do not continue past a nonzero exit unnoticed.

```powershell
conda run --no-capture-output -n quonitron-manim-render python -m compileall -q src scripts examples tests
conda run --no-capture-output -n quonitron-manim-render python scripts/validate_catalog.py
conda run --no-capture-output -n quonitron-manim-render python -m pip check
conda run --no-capture-output -n quonitron-manim-render python -m pytest -ra
conda run --no-capture-output -n quonitron-manim-render python -m pytest -m render -ra
conda run --no-capture-output -n quonitron-manim-render python scripts/verify_renders.py
conda run --no-capture-output -n quonitron-manim-render python scripts/verify_renders.py --only themed --quality production
conda run --no-capture-output -n quonitron-manim-render python scripts/execute_environment_notebook.py
```

Low quality is 480p15. Production verification uses the actual project setting
**1920×1080, 30 fps**, not Manim's `-qh` preset (which may use a different fps).
The full notebook/backend render may take several minutes. Backend execution is
not VS Code playback verification. Artifacts/logs/JSON summaries and timestamped
frames are under `media/environment-verification/`; notebook artifacts under
`media/notebook-environment/`. No successful render is inferred from an old file.

A manual, opt-in Windows GitHub Actions workflow is included at
`.github/workflows/windows-render-check.yml`; after these changes are published,
run **Windows rendering environment check** from Actions. It does not mask failing
render tests. It has **not** been run by adding the file here, and a Windows runner
still cannot certify playback on your PC.

## 7. Troubleshooting by actual failure

- **Conda cannot solve:** save the solver output; do not run pip on top to force
  incompatible compiled versions. Check `conda --version` and internet access to
  Conda-forge, update Miniforge's base package manager if appropriate, then retry
  with a fresh environment name. This sandbox could inspect the historical
  package recipe but could not perform a Windows Conda solve.
- **`No module named quonitron_manim`:** verify `sys.executable`; in THAT environment
  run `python -m pip install --no-deps --no-build-isolation -e .` from this repo.
- **`No module named manim` / wrong Manim:** use `python -m manim --version` and
  `python -c "import manim; print(manim.__version__, manim.__file__)"` in the selected
  environment. A different terminal's `manim` command may point elsewhere.
- **NumPy ABI / `_ARRAY_API` / SciPy error:** do not downgrade to NumPy 1.x for
  Manim 0.19. Recreate a fresh environment from the reference file. Avoid mixing
  pip binary upgrades with Conda's native packages.
- **Cairo/Pango DLL load failure:** `conda list -n quonitron-manim-render` should show
  pycairo, cairo, manimpango and pango; launch from the activated prompt, check the
  chosen kernel. Don't add system GTK DLLs ahead of Conda DLLs or download random
  DLLs. The verifier paints a Cairo surface, lists fonts, and constructs real Text.
- **`pkg-config` or `Python.h` failure on Windows:** you likely entered a pip source
  build instead of the prebuilt Conda route. Stop and inspect the environment. A
  Windows Conda installation does not need the Debian development headers.
- **FFmpeg missing:** `conda run -n quonitron-manim-render ffmpeg -version`. Use
  Conda's ffmpeg package in the same environment. FFprobe is optional here; full
  FFmpeg decode checks are used even without it.
- **LaTeX/dvisvgm not found:** optional for these demos; EquationText falls back to
  plain Text. For genuine typeset TeX, install MiKTeX or TeX Live and dvisvgm using
  their official installers, verify `latex --version` and `dvisvgm --version`, then
  restart VS Code to pick up PATH changes. Do not install TeX just to draw captions.
- **Fonts missing:** Conda's font packages and Windows fallback fonts are used by
  the existing resolver. Check the verifier's actual Pango font list; font changes
  can change geometry, so rerender and inspect, not merely rerun unit tests.
- **Layout preflight / animation exception:** not necessarily environment failure.
  Preserve the scene traceback and generated frames. Existing overlap repairs are
  not visually certified in this sandbox. Do not weaken tests to hide these errors.
- **Partial render output:** inspect `render.log` and `decode.log`; a missing,
  empty, corrupt or non-decodable video is a failure. Frame extraction failure
  also prevents verification success.

## 8. Recreate / lock without overwriting environments

After successful local verification, save an exact **win-64** Conda package lock:

```powershell
New-Item -ItemType Directory -Force .local-environment-locks | Out-Null
conda list -n quonitron-manim-render --explicit | Set-Content -Encoding ascii .local-environment-locks\win-64-explicit.txt
# Inspect the file for the @EXPLICIT header and package URLs before using it.
# Recreate under a FRESH name (never delete your working environment):
conda create -n quonitron-manim-render-recreated --file .local-environment-locks\win-64-explicit.txt
conda run -n quonitron-manim-render-recreated python -m pip install --no-deps --no-build-isolation -e .
conda run --no-capture-output -n quonitron-manim-render-recreated python scripts/verify_environment.py
```

The editable repository is deliberately not in Conda's explicit lock. Use the
same Git revision for exact source reproduction. Do not use this win-64 lock on
Linux/WSL. Inspect exported files before sharing: custom channel URLs can contain
private information. Local locks, environments, movies, frames and executed
notebooks are gitignored.

### WSL2 fallback (separate environment)

Enable/install WSL2 and Ubuntu using Microsoft's instructions. In VS Code use
**Remote-WSL**, and keep the checkout and environment in the WSL filesystem. On a
supported Ubuntu with Python 3.11 available:

```bash
sudo apt-get update
sudo apt-get install -y python3.11-dev python3.11-venv libcairo2-dev libpango1.0-dev pkg-config ffmpeg fonts-dejavu-core
python3.11 -m venv .venv-render-wsl  # fresh name only
source .venv-render-wsl/bin/activate
python -m pip install -r requirements-render.txt
python -m pip install --no-deps -e .
python scripts/verify_environment.py
```

Ubuntu releases differ in their default Python. If `python3.11-dev` is not in your
release's official repositories, do not add an arbitrary PPA: use a separate
Linux Miniforge environment with the same compatible spec (not a win-64 explicit
lock), or the provided Python 3.11 Dev Container. Never share a Windows Conda
prefix or `.venv` with WSL.

## References actually inspected

- [Manim CE 0.19.0 package metadata](https://pypi.org/pypi/manim/0.19.0/json).
- [0.19.0 changelog: PyAV replaces external FFmpeg](https://github.com/ManimCommunity/manim/blob/v0.19.0/docs/source/changelog/0.19.0-changelog.rst).
- [Versioned Conda installation guide](https://github.com/ManimCommunity/manim/blob/v0.19.0/docs/source/installation/conda.rst).
- [Conda-forge 0.19.0 recipe inspected at its actual revision](https://github.com/conda-forge/manim-feedstock/blob/cd467957651b16876fa8911964774bdbbda17068/recipe/recipe.yaml).
