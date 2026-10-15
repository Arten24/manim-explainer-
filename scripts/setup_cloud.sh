#!/usr/bin/env bash
# Linux cloud setup only. Never touches the user's Windows PC.
set -euo pipefail
cd "$(dirname "$0")/.."
ENV_DIR="${1:-.venv-cloud}"
PYTHON="${PYTHON:-python3.11}"
if [[ -e "$ENV_DIR" && ! -x "$ENV_DIR/bin/python" ]]; then
  echo "Refusing to overwrite non-environment path: $ENV_DIR" >&2; exit 2
fi
if [[ -x "$ENV_DIR/bin/python" ]]; then
  "$ENV_DIR/bin/python" -c 'import sys; assert sys.version_info[:2] == (3, 11), "Use a separate Python 3.11 environment"'
fi
# apt-get can otherwise return 0 even when EVERY index download failed.
sudo apt-get update --error-on=any -o Acquire::Retries=0 -o Acquire::http::Timeout=15 -o Acquire::https::Timeout=15
sudo apt-get install -y --no-install-recommends \
  libcairo2-dev libpango1.0-dev pkg-config python3-dev python3-venv ffmpeg fonts-dejavu-core
if [[ ! -x "$ENV_DIR/bin/python" ]]; then "$PYTHON" -m venv "$ENV_DIR"; fi
"$ENV_DIR/bin/python" -m pip install -r requirements-render.txt
"$ENV_DIR/bin/python" -m pip install --no-deps -e .
export PATH="$PWD/$ENV_DIR/bin:$PATH"
"$ENV_DIR/bin/python" scripts/verify_environment.py --json media/cloud-verification/dependencies.json
"$ENV_DIR/bin/python" scripts/verify_renders.py --only minimal themed
