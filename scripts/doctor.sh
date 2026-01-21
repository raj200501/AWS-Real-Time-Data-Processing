#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "RTAP Doctor"
echo "==========="

python_version=$(python - <<'PY'
import sys
print("{}.{}.{}".format(*sys.version_info[:3]))
PY
)

echo "Python: $python_version"

echo "Checking dependencies..."
python - <<'PY'
import importlib
required = ["boto3", "pytest", "yaml"]
missing = [name for name in required if importlib.util.find_spec(name) is None]
if missing:
    print("Missing:", ", ".join(missing))
    raise SystemExit(1)
print("Dependencies OK")
PY

echo "Environment defaults:"
python - <<'PY'
import os
print("USE_FAKE_AWS=", os.getenv("USE_FAKE_AWS", "1"))
print("RTAP_LOG_FORMAT=", os.getenv("RTAP_LOG_FORMAT", "text"))
print("RTAP_METRICS=", os.getenv("RTAP_METRICS", "1"))
print("RTAP_OTEL=", os.getenv("RTAP_OTEL", "0"))
PY

echo "Doctor complete."
