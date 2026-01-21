"""Built-in plugins for the RTAP pipeline."""

from __future__ import annotations

from dataclasses import dataclass

from .base import EventPayload


@dataclass
class NormalizeTemperaturePlugin:
    name: str = "normalize_temperature"

    def process(self, payload: EventPayload) -> EventPayload:
        normalized = (
            (payload.temperature - 32) * 5 / 9
            if payload.temperature > 60
            else payload.temperature
        )
        return EventPayload(
            sensor_id=payload.sensor_id,
            temperature=round(normalized, 2),
            humidity=payload.humidity,
            timestamp=payload.timestamp,
        )


@dataclass
class HumidityClampPlugin:
    name: str = "clamp_humidity"

    def process(self, payload: EventPayload) -> EventPayload:
        clamped = min(max(payload.humidity, 0.0), 100.0)
        return EventPayload(
            sensor_id=payload.sensor_id,
            temperature=payload.temperature,
            humidity=round(clamped, 2),
            timestamp=payload.timestamp,
        )
