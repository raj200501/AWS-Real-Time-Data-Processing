#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${ROOT_DIR}:${ROOT_DIR}/src:${PYTHONPATH:-}"
export USE_FAKE_AWS="${USE_FAKE_AWS:-1}"
export RTAP_DEMO_MODE="1"

cd "$ROOT_DIR"

output=$(python -m rtap.cli demo --events 8)
status=$?

echo "$output"

if echo "$output" | grep -q "PASS"; then
  echo "Demo succeeded."
  exit 0
fi

echo "Demo failed."
exit $status
