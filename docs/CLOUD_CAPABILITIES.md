# Cloud development verification

Verification in progress; this is not a successful-render claim.

- Actual checkout: Arten24/manim-explainer-, branch arena/9c18e37e-manim-explainer.
- GitHub read access and repository push permission verified by API (ADMIN).
- Actions repository-permission settings API returns 403 despite viewer permission.
- Workspace: Debian 12 x86-64, Python 3.11.2. Existing .venv is preserved.
- Isolated .venv-render-check contains pinned unit/notebook packages, NumPy 2.2.6,
  SciPy 1.15.3 and PyAV 13.1.0. FFmpeg 7.0.2 from the imageio-ffmpeg wheel works.
- Cairo/Pango native development packages and Python.h are absent. Debian apt
  hosts are unreachable; update emits failed fetches (plain apt-get can misleadingly
  exit zero). setup_cloud.sh uses --error-on=any and fails honestly.
- GitHub Actions runs/log metadata are accessible; actual log/artifact download
  redirects to external storage hosts blocked by this workspace's host allowlist.
- Cloud verification workflow uses an Ubuntu runner for actual renders and emits
  compact JSON/JPEG frame evidence through the accessible GitHub Checks API.
  Adding this workflow is not proof it ran successfully; results will be recorded
  after the actual push and run.

No software on the user's Windows PC has been accessed or changed.
