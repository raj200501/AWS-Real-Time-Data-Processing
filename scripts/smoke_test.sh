#!/bin/bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"
export USE_FAKE_AWS=${USE_FAKE_AWS:-1}
python -m pytest -q
