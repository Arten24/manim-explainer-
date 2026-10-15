# Verified cloud development capabilities — 2026-10-15

> **Final status:** GitHub read/edit/commit/push and cloud-runner rendering are
> verified. Final code: `b082fc3`. **Cloud: 99 passed / 0 failed / 0 skipped**;
> separate renderer job: **11 passed / 0 failed / 0 skipped**; notebook: **9/9
> code cells, 7 video HTML outputs, no errors**. Interactive Arena native rendering
> remains blocked; rendering works on the actual GitHub-hosted Linux runner.
> Known visual defects remain. No Windows PC changes and no Part 5.

## Boundary: two different cloud environments

**No access to or changes on the user's Windows PC. No Part 5 started.**

1. **Interactive Arena workspace:** Debian 12 x86-64, Python 3.11.2, repository
   `/home/user/manim-explainer-`. Existing `.venv` was preserved. The separate
   `.venv-render-check` supports development, tests, Git, schema/subtitle exports,
   IPython and Jupyter, but **does not have a working Manim renderer**.
2. **Actual GitHub Actions Linux runner:** Ubuntu 22.04, x86-64, Python 3.11.17,
   reference Manim CE 0.19.0 installed and independently verified. It **does render**
   the project. This is not a claim that native rendering works inside Arena.

## GitHub access actually exercised

- Actual origin: `https://github.com/Arten24/manim-explainer-.git`.
- Session branch: `arena/9c18e37e-manim-explainer`; no other branch was created,
  switched to, or pushed. Read/edit/test/commit/push capabilities were exercised.
- `gh auth status` succeeded; `gh repo view` reported viewerPermission `ADMIN`;
  repository metadata reported pull/push/admin true. Authentication was already
  configured; no credentials were requested or stored.
- Successful commits/pushes were verified against `git ls-remote`, not inferred.
- GitHub Actions workflow/run/job/check metadata can be read. Push-triggered
  workflows actually ran. Repository Actions-permissions and run-cancellation
  endpoints returned **403 Resource not accessible by integration**: repository
  viewer permission does not imply every installed-app token permission.
- The optional Arena GitHub connector lookup returned unsupported; native `git`
  and `gh` still work. This is not a disconnected-repository claim.
- Downloading logs/artifacts redirects to external storage hosts blocked by the
  workspace host allowlist. Error URLs can contain signed query parameters;
  they are not included in this report. Standard CI artifacts are retained, and
  compact reports/frame copies are additionally published via the accessible
  GitHub Checks API. The read-only `fetch_ci_evidence.py` retrieves those copies.

## Dependencies installed and independently checked

| Dependency | Interactive workspace | Actual Actions runner |
|---|---|---|
| Python | 3.11.2; executable in `.venv-render-check/bin/python` | 3.11.17; `/opt/hostedtoolcache/Python/3.11.17/x64/bin/python` |
| Manim CE | **Missing**; install attempt failed building Cairo | **0.19.0**; import and both module/CLI version probes passed |
| NumPy | 2.2.6 import passed | 2.2.6 import passed |
| SciPy | 1.15.3 import passed | 1.15.3 import passed |
| PyAV | 13.1.0; libx264 encoder opened | 13.1.0; libx264 encoder opened, actual movies encoded |
| FFmpeg | 7.0.2-static from imageio-ffmpeg 0.6.0 in the isolated env; environment-local symlink verified | Ubuntu FFmpeg 4.4.2; version and complete movie decode passed |
| Cairo / pycairo | Absent; native development library unavailable | Native Cairo 1.16.0, pycairo 1.29.2; painted surface verified |
| Pango / manimpango | Absent; build also failed on missing Python.h | manimpango 0.7.0; 14 fonts found, actual Manim Text constructed |
| pkg-config / Python headers | Missing; required for these Linux source builds | Native prerequisites installed successfully with apt |
| IPython / ipykernel | 8.32.0 / 6.29.5 imports passed | Same versions passed |
| nbformat / nbclient | 5.10.4 / 0.10.2 imports passed | Same versions passed |
| jsonschema / pytest | 4.23.0 / 8.3.5 imports passed | Same versions passed |
| Git | 2.39.5 locally; actual GitHub read and push verified | Git/checkout available |
| LaTeX / dvisvgm | Not installed | Not installed; optional EquationText fallback used |
| VS Code / browser frontend | Not available | Not available; no claim of inline browser playback |

Manim 0.19 uses PyAV for encoding; external FFmpeg is required by this repository's
verification/extraction scripts, not by that Manim encoder itself. Cairo/Pango are
required for the implemented text scenes. No GPU/OpenGL or LaTeX installation was
needed for these Cairo previews.

### Why Arena native installation is still blocked

`sudo -n true` succeeded, so this is **not** a missing-administrator diagnosis.
`apt-get update` could not connect to Debian package hosts. Plain apt-get misleadingly
returned zero with failed-fetch warnings; `setup_cloud.sh` uses `--error-on=any`
and correctly returned **100**. Installing Manim 0.19.0 via pip failed because
Cairo/pkg-config was unavailable. Independent manimpango installation failed at
`fatal error: Python.h: No such file or directory`. Headers/native libraries are
not present in the workspace. No fake bindings or arbitrary DLL substitutes were
used. The practical renderer is the verified GitHub-hosted runner; direct Arena
rendering needs access to native package hosts or a pre-provisioned render image.

## Real renders and frame inspection

Actual run: https://github.com/Arten24/manim-explainer-/actions/runs/38704111956

Verified source SHA: `bf8750acc4d4f6312b6c862af0a3ae7d265ae3cd`.
The API-readable report/check `116322204445` contains the actual renderer commands,
exit codes, nonempty movie sizes, decode results and extracted-frame paths.
That **preliminary** check was marked failure solely because tests had not yet
been added to the report; it does not mean the eight reported renders failed.
Subsequent infrastructure distinguishes preliminary reports as neutral.

| Scene | Actual result | MP4 bytes |
|---|---|---:|
| MinimalRenderCheck | Rendered, fully decoded, frames extracted | 13,682 |
| ThemeSubtitleRenderCheck | Rendered, fully decoded, frames extracted | 29,865 |
| VariableStoresAValue (Part 1) | Rendered, fully decoded, frames extracted | 185,291 |
| VariableMemoryTimeline (Part 2) | Rendered, fully decoded, frames extracted | 516,695 |
| CodeToMemoryJourney (Part 3) | Rendered, fully decoded, frames extracted | 549,462 |
| AssignmentInType (Part 4) | Rendered, fully decoded, frames extracted | 702,656 |
| LayoutRepairExercise | Rendered, fully decoded, frames extracted | 116,501 |
| ThemeSubtitleRenderCheck, requested 1920×1080/30 fps | Rendered, fully decoded, frame extracted | 66,943 |

Preview commands used `-ql` (480p15). Production command explicitly used
`-r 1920,1080 --fps 30`. The frame API transport JPEG-compresses actual extracted
PNG frames and may downsample production images; no full-movie playback in Arena
or browser verification is implied by these copies. The newer API transport also records pre-compression source dimensions:
production sample check `116328831277` verified **1920×1080** source pixels;
preview check `116328845290` recorded **854×480**. All original movies/PNGs are
normal CI artifacts, not committed repository files.

**Actual visual findings** from retrieved frames, not just bounding boxes:

- Part 1 at 20 s: name/value readable inside the card, caption separated below.
- Themed smoke at 1.5 s: title, lesson, circle and subtitle have clear separation.
- Part 4 at 9, 28, 53 s: subtitle band stays separated; title hierarchy and lesson
  region are visible. At 28 s the colored identifier and following words look
  tightly joined (`scoreis`, `10is`); typography needs follow-up. The 53 s sample
  still shows the recap, so it does not certify the later paragraph.
- **Part 2 at 95 s: solid blue card; name/value labels are not visible.** This is
  a real application rendering defect to investigate, not missing dependencies.
- **Part 3 at 65 s: `score = 10` overlaps the recap sentence.** Source-object
  lifecycle/transition behavior needs investigation; rendering success did not
  prove overlap safety. At 22.8 and 41 s, the sampled card/code transition remains
  separated from the caption.
- Overlap exercise at 3.1, 3.6, 5 s: the blank midpoint corresponds to the sequential
  fade; final diagram, value and label are visible above the caption. Arrow crosses
  the panel border toward the slot. The later 1 s sample shows the long paragraph wrapping into four readable
  lines inside the frame, separated from the caption. No exhaustive pixel
  validation is claimed.
- Later camera samples at 49/54 s show the full table and close-up respectively.
  At 54 s the focused value remains visible, neighboring context is cropped,
  and the subtitle remains at the bottom of the viewport. The full-table sample
  also shows a stray white code fragment beneath/between cells, consistent with
  the later unresolved transition/lifecycle issue.

These findings supersede only the **no-render-evidence limitation** in the earlier
historical overlap audit. They do not establish that all overlaps are fixed.
No scene redesign was performed during this cloud setup task.

## Tests and notebook status

- Local full suite: **88 passed, 0 failed, 11 skipped**. All skips require the
  missing Cairo/Pango/Manim renderer; no skipped render is counted as successful.
- Local timeline/subtitle/segmentation subset: **19 passed** (included above).
- Catalog JSON/schema/Python references: **103 components validated**.
- Syntax compilation and `pip check`: passed.
- Independently validated and exported actual variable, journey and text timelines:
  **34, 11 and 11 cues**, respectively; nonempty SRT/VTT created under ignored media.
- GitHub Tests workflow at `911d061` succeeded, including its renderer job:
  https://github.com/Arten24/manim-explainer-/actions/runs/38703125370
- GitHub Tests workflow at `bf8750a` also succeeded. Its unit matrix covers Python
  3.10/3.11/3.12. The full cloud suite at `8d58ea0` independently reported **98 passed, 0 failed,
  0 errors, 0 skipped** in JUnit (API check `116331439527`). This includes the
  render-dependent tests. The initial `911d061` run also reported 98/0/0/0, before
  its combined job budget was exhausted later during notebook execution.
- Local strict environment notebook execution correctly **failed at diagnostics**
  with BLOCKED (missing Manim/Cairo/Pango). It did not silently skip to success.
- **Actual notebook backend execution succeeded** in the separate notebook job:
  **9/9 code cells executed, zero errors, 7 video HTML outputs**. API check
  `116328872015` on `8d58ea0` records those counts. The strict notebook verified
  rendered MP4, full decode, extracted frames and embedded HTML. Browser/VS Code
  playback remains a human/frontend check.
- Successful complete run: https://github.com/Arten24/manim-explainer-/actions/runs/38706426574
  (both main verification and notebook jobs succeeded).
- Earlier combined workflows reached the 25-minute job budget during notebook
  execution after tests/renders passed. Notebook execution was separated into a
  parallel, bounded job, and superseded verification uses concurrency cancellation.
- A legacy renderer job on floating `ubuntu-latest` failed after the 180-second
  per-test policy was introduced; its detailed log could not be downloaded here.
  This is not claimed as a diagnosed application or dependency defect. That job
  was aligned to the already-proven Ubuntu 22.04 runner and given API-readable
  JUnit evidence. The final results below include the actual timeout diagnosis, narrow performance repair and successful rerun.

## Reproducible cloud tooling

- `requirements-render.txt`: compatible pinned reference Python stack; not a
  complete transitive hash lock. pytest-timeout bounds future CI tests.
- `scripts/setup_cloud.sh`: Debian/Ubuntu native setup, separate environment,
  independent checks and actual smoke renders; preserves existing environments.
- `scripts/verify_environment.py`: real imports, Cairo paint, fonts/Text, encoder,
  executable/kernel probes; fails clearly when blocked.
- `scripts/verify_renders.py`: fresh output directories, real process exit,
  nonempty movie, complete FFmpeg decode and timestamped frame extraction.
- `scripts/execute_environment_notebook.py`: strict backend execution; outputs
  stored in ignored media, not in the tracked notebook.
- `scripts/publish_ci_evidence.py` / `fetch_ci_evidence.py`: API transport for
  reports and JPEG frame copies when standard artifact hosts are inaccessible.
- `.github/workflows/cloud-verification.yml`: required Linux functionality probes,
  all demos, production smoke, complete tests, notebook execution and evidence.
  A per-test timeout, job timeout and future-run concurrency limit resource use.
- Existing Tests renderer no longer uses continue-on-error; native fonts and
  reference versions are installed. Render preview uses the same reference pins.
- `.gitignore`: all virtual environments, caches, media, local locks and secrets
  remain excluded. No generated movie or credential was committed.

The prior interrupted Windows setup files were preserved, not executed on the
user's PC. They are not evidence about the user's installed environment.

## Remaining limits / required follow-up

1. Native rendering inside the interactive Arena workspace remains blocked by
   package-host access. Use the actual verified Actions runner until that changes.
2. Full logs/videos cannot be downloaded into Arena via the standard artifact
   route. Compact frame/report retrieval through GitHub's API is verified.
3. Actions administration/cancellation APIs return 403. Do not infer those rights
   from viewerPermission ADMIN; no credentials should be pasted into chat.
4. No Windows software configuration or browser/VS Code inline playback was
   attempted. Backend execution and generated HTML are different claims.
5. The observed Part 2/Part 3 rendering defects and Part 4 spacing need an explicit
   application repair task. This setup does not grant visual acceptance.
6. High-resolution geometry-only tests were unnecessarily costly. Their assertions
   are preserved; dry renders now use preview quality. CI test/job timeouts expose
   excessive runtime rather than leaving tests unbounded or removing assertions.

No Part 5 or unrelated library feature was started.

## Changes, commits, and reproducible evidence retrieval

Cloud-specific changes: Linux bootstrap, pinned CI stack, cloud and legacy renderer
workflows, independent notebook job, API-readable test/frame reporting and fetching,
preview-quality geometry checks (same assertions), documentation and diagnostics.
The initial `911d061` commit also preserved the previous task's uncommitted overlap
repairs and interrupted Windows setup files; those are not new Windows-PC actions.

Verified pushed implementation commits on the session branch:
`911d061`, `bf8750a`, `47796db`, `8d58ea0`, `5df2936`, `2821e09`, `b082fc3`.
There were no changes to `src/`, `examples/`, or `notebooks/` between `911d061`
and `5df2936`. A subsequent narrow camera-caption performance repair is described
below; no new component, animation feature, timeline model, or Part was added.
No PR was opened or merged. The final documentation-only commit skips duplicate
CI work; it does not skip any application change's verification.

For an actual full commit SHA from `git rev-parse` or the run API:

```bash
gh run list --branch arena/9c18e37e-manim-explainer
gh run watch <actual-run-id> --exit-status
python scripts/fetch_ci_evidence.py --sha <actual-full-commit-sha>
```

Full cumulative file list relative to the original session checkout (including
preserved prior work, not just this cloud setup):

- `.devcontainer/devcontainer.json`
- `.github/workflows/cloud-verification.yml`
- `.github/workflows/render-preview.yml`
- `.github/workflows/tests.yml`
- `.github/workflows/windows-render-check.yml`
- `.gitignore`
- `README.md`
- `docs/CLOUD_CAPABILITIES.md`
- `docs/OVERLAP_AUDIT.md`
- `docs/WINDOWS_SETUP.md`
- `environment.windows.yml`
- `examples/README.md`
- `examples/environment_smoke.py`
- `examples/foundation_demo.py`
- `examples/journey_demo.py`
- `examples/layout_audit_demo.py`
- `examples/motion_timeline_demo.py`
- `examples/text_typography_demo.py`
- `notebooks/environment_render_test.ipynb`
- `notebooks/overlap_repair_lab.ipynb`
- `requirements-render.txt`
- `scripts/execute_environment_notebook.py`
- `scripts/fetch_ci_evidence.py`
- `scripts/publish_ci_evidence.py`
- `scripts/render_layout_audit.py`
- `scripts/setup_cloud.sh`
- `scripts/setup_windows.ps1`
- `scripts/verify_environment.py`
- `scripts/verify_renders.py`
- `src/quonitron_manim/components/foundation/section_heading.py`
- `src/quonitron_manim/components/foundation/subtitle_overlay.py`
- `src/quonitron_manim/components/foundation/title_card.py`
- `src/quonitron_manim/components/foundation/variable_store.py`
- `src/quonitron_manim/components/text/base.py`
- `src/quonitron_manim/components/text/blocks.py`
- `src/quonitron_manim/core/base_scene.py`
- `src/quonitron_manim/core/text.py`
- `src/quonitron_manim/design/layout.py`
- `tests/test_environment_setup.py`
- `tests/test_layout_audit.py`

## Diagnosed renderer timeout and narrow repair

API-readable JUnit evidence on `5df2936` (check `116336110638`) exposed **8 passed,
2 failed, 0 skipped** in the isolated renderer job. Both failures were 180-second
timeouts in the Part 3 camera journey, not missing native dependencies. The trace
showed `SubtitleOverlay._tick -> mob.become(projected) -> deepcopy`: every frame,
even during static holds, copied the full caption's SVG/glyph graph. Merely pinning
the legacy runner to Ubuntu 22.04 did not fix it; no such causal claim is made.

`2821e09` replaces that expensive per-frame clone with the equivalent incremental
camera translation/scale, does nothing for an unchanged viewport, and resets the
projection on every cue replacement. The existing overlay API, font size, layout,
timeline clock and narration are preserved. **The 180-second cap was not raised.**

Actual renderer timings after the repair (JUnit check `116339124932`):

- Journey endpoint-geometry test: **39.547 s**, previously timeout at **180.027 s**.
- Journey actual MP4 render test: **42.333 s**, previously timeout at **180.013 s**.
- All ten previously existing render tests passed; the newly added camera-point
  regression initially failed because it assumed `Manim.become` preserves SVG
  control-point counts across different text. Real Manim aligns those subpaths.
  This was a test-reference error, not a failed movie render.
- `b082fc3` corrects that reference: verify replacement canonical bounds, then
  assert every actual post-restyle point's affine mapping. Earlier zoom/pan/restore
  point checks and the assertions prohibiting per-frame `copy`/`become` remain.
  No test was removed or made a successful skip.

### Final verified results

Verified code commit: `b082fc3aa5b5ab990c651580149abe927c464c91`.

- Full cloud suite: **99 passed, 0 failed, 0 errors, 0 skipped**;
  API check `116343730605`.
- Separate renderer job: **11 passed, 0 failed, 0 errors, 0 skipped**;
  API check `116341898779`. The new full-point/bounds camera regression passed.
- Notebook: **9/9 code cells executed, no errors, 7 video HTML outputs**;
  API check `116341748695`.
- All seven preview scenes plus the production smoke render completed, produced
  nonempty MP4s, passed complete FFmpeg decoding and extracted nonempty frames.
- Local suite: **88 passed, 0 failed, 11 skipped** (renderer unavailable locally).
- The 180-second per-test limit remains in place; failures were repaired rather
  than hidden by dropping tests or raising the limit.

Actual final runs:
https://github.com/Arten24/manim-explainer-/actions/runs/38710262977
and https://github.com/Arten24/manim-explainer-/actions/runs/38710262971.

Browser playback is still not verified. The known Part 2 visibility and Part 3
recap collisions were visually rechecked after the performance repair and remain;
they are deliberately not disguised by these passing environment tests.
