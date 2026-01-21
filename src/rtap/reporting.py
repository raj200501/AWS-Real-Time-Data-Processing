"""Analytics report generation for RTAP demo data."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict, Iterable, List

import boto3
import rtap.aws  # noqa: F401

from .plugins.base import EventPayload


@dataclass
class AnalyticsReport:
    """Summarize processed events and export artifacts."""

    events: List[EventPayload]

    @staticmethod
    def from_json_lines(text: str) -> "AnalyticsReport":
        events: List[EventPayload] = []
        for line in text.splitlines():
            if not line.strip():
                continue
            payload = json.loads(line)
            events.append(
                EventPayload(
                    sensor_id=int(payload["sensor_id"]),
                    temperature=float(payload["temperature"]),
                    humidity=float(payload["humidity"]),
                    timestamp=int(payload["timestamp"]),
                )
            )
        return AnalyticsReport(events)

    @staticmethod
    def from_s3(bucket: str, key: str) -> "AnalyticsReport":
        response = boto3.client("s3").get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return AnalyticsReport.from_json_lines(body)

    @staticmethod
    def from_events(events: Iterable[EventPayload]) -> "AnalyticsReport":
        return AnalyticsReport(list(events))

    def summary(self) -> Dict[str, float | int]:
        if not self.events:
            return {"event_count": 0}
        total_temp = sum(event.temperature for event in self.events)
        total_humidity = sum(event.humidity for event in self.events)
        temps = [event.temperature for event in self.events]
        humidities = [event.humidity for event in self.events]
        return {
            "event_count": len(self.events),
            "avg_temperature": round(total_temp / len(self.events), 2),
            "avg_humidity": round(total_humidity / len(self.events), 2),
            "min_temperature": min(temps),
            "max_temperature": max(temps),
            "min_humidity": min(humidities),
            "max_humidity": max(humidities),
        }

    def anomalies(
        self, temp_threshold: float = 33.0, humidity_threshold: float = 65.0
    ) -> List[EventPayload]:
        return [
            event
            for event in self.events
            if event.temperature >= temp_threshold
            or event.humidity >= humidity_threshold
        ]

    def sensor_breakdown(self) -> Dict[int, int]:
        breakdown: Dict[int, int] = {}
        for event in self.events:
            breakdown[event.sensor_id] = breakdown.get(event.sensor_id, 0) + 1
        return breakdown

    def to_markdown(self) -> str:
        summary = self.summary()
        breakdown = self.sensor_breakdown()
        anomalies = self.anomalies()
        lines = [
            "# Analytics Report",
            "",
            "## Summary",
            "",
        ]
        for key, value in summary.items():
            lines.append(f"- **{key.replace('_', ' ').title()}**: {value}")
        lines.extend(["", "## Events by Sensor", ""])
        for sensor_id, count in sorted(breakdown.items()):
            lines.append(f"- Sensor {sensor_id}: {count} events")
        lines.extend(["", "## Anomalies", ""])
        if anomalies:
            for event in anomalies:
                lines.append(
                    f"- Sensor {event.sensor_id} at {event.timestamp}: "
                    f"temp {event.temperature}°C, humidity {event.humidity}%"
                )
        else:
            lines.append("- None")
        return "\n".join(lines)

    def write_markdown(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_markdown(), encoding="utf-8")

    def write_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "summary": self.summary(),
            "sensor_breakdown": self.sensor_breakdown(),
            "anomalies": [event.as_dict() for event in self.anomalies()],
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
