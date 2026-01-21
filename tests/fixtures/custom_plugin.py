from dataclasses import dataclass

from rtap.plugins.base import EventPayload


@dataclass
class AddHumidityPlugin:
    name: str = "add_humidity"

    def process(self, payload: EventPayload) -> EventPayload:
        return EventPayload(
            sensor_id=payload.sensor_id,
            temperature=payload.temperature,
            humidity=payload.humidity + 5.0,
            timestamp=payload.timestamp,
        )
