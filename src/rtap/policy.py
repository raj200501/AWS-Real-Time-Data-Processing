"""Policy and safety checks for RTAP events (disabled by default)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Set

from .plugins.base import EventPayload


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    risk: RiskLevel
    reason: str


@dataclass
class PolicyEngine:
    """Simple allow/deny policy for event payloads."""

    max_temperature: float = 40.0
    max_humidity: float = 90.0
    allowed_sensors: Set[int] | None = None

    def evaluate(self, payload: EventPayload) -> PolicyDecision:
        if (
            self.allowed_sensors is not None
            and payload.sensor_id not in self.allowed_sensors
        ):
            return PolicyDecision(False, RiskLevel.high, "sensor not in allowlist")
        if payload.temperature > self.max_temperature:
            return PolicyDecision(False, RiskLevel.high, "temperature above threshold")
        if payload.humidity > self.max_humidity:
            return PolicyDecision(False, RiskLevel.medium, "humidity above threshold")
        return PolicyDecision(True, RiskLevel.low, "within policy")

    @staticmethod
    def from_allowlist(allowlist: Iterable[int]) -> "PolicyEngine":
        return PolicyEngine(allowed_sensors=set(allowlist))
