"""Health check utilities for the RTAP demo pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict


@dataclass(frozen=True)
class HealthStatus:
    status: str
    checks: Dict[str, str]
    timestamp: str


def build_health_status(checks: Dict[str, bool]) -> HealthStatus:
    detailed = {name: ("ok" if value else "fail") for name, value in checks.items()}
    overall = "ok" if all(checks.values()) else "degraded"
    return HealthStatus(
        status=overall,
        checks=detailed,
        timestamp=datetime.now(tz=timezone.utc).isoformat(),
    )
