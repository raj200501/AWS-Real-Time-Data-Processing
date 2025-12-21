"""Minimal YAML stub used for offline tests.
Provides safe_load/dump using json for deterministic behavior."""
import json

def safe_load(stream):
    if isinstance(stream, (str, bytes)):
        data = stream
    else:
        data = stream.read()
    if data is None:
        return None
    try:
        return json.loads(data)
    except Exception:
        return data


def dump(data):
    return json.dumps(data)
