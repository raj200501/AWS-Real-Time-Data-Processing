#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${ROOT_DIR}:${ROOT_DIR}/src:${PYTHONPATH:-}"
export USE_FAKE_AWS="${USE_FAKE_AWS:-1}"

cd "$ROOT_DIR"

echo "==> Running lint checks"
./scripts/lint.sh

echo "==> Running unit tests"
python -m pytest

echo "==> Running smoke tests"
./scripts/smoke_test.sh

echo "==> Running demo"
./scripts/demo.sh

echo "==> Compile check"
python -m compileall -q src

echo "Verification complete."
