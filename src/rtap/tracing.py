"""Trace recorder for offline diagnostics."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


@dataclass
class TraceSpan:
    name: str
    recorder: "TraceRecorder"
    start: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
    fields: Dict[str, Any] = field(default_factory=dict)

    def add_field(self, key: str, value: Any) -> None:
        self.fields[key] = value

    def __enter__(self) -> "TraceSpan":
        self.recorder.record_event(
            "span.start",
            name=self.name,
            timestamp=self.start.isoformat(),
            fields=self.fields,
        )
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        end = datetime.now(tz=timezone.utc)
        payload = {
            "name": self.name,
            "timestamp": end.isoformat(),
            "duration_ms": (end - self.start).total_seconds() * 1000,
            "fields": self.fields,
        }
        if exc is not None:
            payload["error"] = str(exc)
        self.recorder.record_event("span.end", **payload)


@dataclass
class TraceRecorder:
    """Append-only JSONL trace recorder."""

    path: Optional[Path] = None
    enabled: bool = False

    def record_event(self, event_type: str, **payload: Any) -> None:
        if not self.enabled or not self.path:
            return
        event = {
            "event": event_type,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "payload": payload,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False))
            handle.write("\n")

    def span(self, name: str, **fields: Any) -> TraceSpan:
        return TraceSpan(name=name, recorder=self, fields=dict(fields))

    def read_events(self) -> list[dict[str, Any]]:
        if not self.path or not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]


@dataclass
class TraceExporter:
    """Export traces to Markdown for quick sharing."""

    events: Iterable[Dict[str, Any]]

    def to_markdown(self) -> str:
        lines = [
            "# Trace Export",
            "",
            "| Event | Timestamp | Details |",
            "| --- | --- | --- |",
        ]
        for event in self.events:
            payload = json.dumps(event.get("payload", {}), ensure_ascii=False)
            lines.append(
                f"| {event.get('event')} | {event.get('timestamp')} | `{payload}` |"
            )
        return "\n".join(lines)
