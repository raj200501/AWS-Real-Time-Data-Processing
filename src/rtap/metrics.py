"""In-process metrics helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Dict, Iterable, Optional


@dataclass
class Timer:
    """Context manager for timing operations."""

    registry: "MetricRegistry"
    name: str
    start: float = field(default_factory=time.perf_counter)

    def __enter__(self) -> "Timer":
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        duration = time.perf_counter() - self.start
        self.registry.observe(self.name, duration)


@dataclass
class MetricSnapshot:
    counters: Dict[str, int]
    timers: Dict[str, list[float]]

    def summary(self) -> Dict[str, float]:
        summary: Dict[str, float] = {}
        for name, values in self.timers.items():
            if not values:
                continue
            summary[f"{name}.count"] = float(len(values))
            summary[f"{name}.avg_s"] = sum(values) / len(values)
            summary[f"{name}.max_s"] = max(values)
        for name, count in self.counters.items():
            summary[f"{name}.count"] = float(count)
        return summary


@dataclass
class MetricRegistry:
    """Simple metrics registry for counters and timers."""

    enabled: bool = True
    counters: Dict[str, int] = field(default_factory=dict)
    timers: Dict[str, list[float]] = field(default_factory=dict)

    def increment(self, name: str, value: int = 1) -> None:
        if not self.enabled:
            return
        self.counters[name] = self.counters.get(name, 0) + value

    def observe(self, name: str, duration: float) -> None:
        if not self.enabled:
            return
        self.timers.setdefault(name, []).append(duration)

    def time(self, name: str) -> Timer:
        return Timer(self, name)

    def snapshot(self) -> MetricSnapshot:
        return MetricSnapshot(
            counters=dict(self.counters),
            timers={k: list(v) for k, v in self.timers.items()},
        )

    def merge(self, other: "MetricRegistry") -> None:
        for name, count in other.counters.items():
            self.counters[name] = self.counters.get(name, 0) + count
        for name, values in other.timers.items():
            self.timers.setdefault(name, []).extend(values)

    def reset(self) -> None:
        self.counters.clear()
        self.timers.clear()


def format_metrics(
    snapshot: MetricSnapshot, prefix: str = "rtap", precision: Optional[int] = None
) -> str:
    items = sorted(snapshot.summary().items())
    decimals = 4 if precision is None else precision
    return "\n".join(
        (
            f"{prefix}.{name}: {value:.{decimals}f}"
            if name.endswith(".avg_s") or name.endswith(".max_s")
            else f"{prefix}.{name}: {value:.0f}"
        )
        for name, value in items
    )


def merge_snapshots(snapshots: Iterable[MetricSnapshot]) -> MetricSnapshot:
    registry = MetricRegistry()
    for snapshot in snapshots:
        registry.merge(
            MetricRegistry(counters=snapshot.counters, timers=snapshot.timers)
        )
    return registry.snapshot()
