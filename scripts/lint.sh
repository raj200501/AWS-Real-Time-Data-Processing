#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${ROOT_DIR}:${ROOT_DIR}/src:${PYTHONPATH:-}"

cd "$ROOT_DIR"

echo "==> Python syntax check"
python -m compileall -q src tests

echo "==> Optional formatter check"
if python -m black --version >/dev/null 2>&1; then
  python -m black --check src tests
else
  echo "black not installed; skipping format check"
fi

echo "==> Optional linter"
if python -m ruff --version >/dev/null 2>&1; then
  python -m ruff check src tests
else
  echo "ruff not installed; skipping lint check"
fi
