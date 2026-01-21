"""Plugin interface for RTAP data processing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Protocol


@dataclass
class EventPayload:
    sensor_id: int
    temperature: float
    humidity: float
    timestamp: int

    def as_dict(self) -> Dict[str, float | int]:
        return {
            "sensor_id": self.sensor_id,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "timestamp": self.timestamp,
        }


class Plugin(Protocol):
    name: str

    def process(self, payload: EventPayload) -> EventPayload:
        """Return a transformed payload."""
        raise NotImplementedError
