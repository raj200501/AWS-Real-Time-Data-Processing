"""Optional OpenTelemetry scaffolding (disabled by default)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class OtelConfig:
    enabled: bool
    service_name: str = "rtap"
    attributes: Dict[str, str] = None

    def is_enabled(self) -> bool:
        return bool(self.enabled)

    def to_resource_attributes(self) -> Dict[str, str]:
        base = {"service.name": self.service_name}
        if self.attributes:
            base.update(self.attributes)
        return base


class OtelScaffold:
    """No-op scaffold for environments without OpenTelemetry installed."""

    def __init__(self, config: OtelConfig) -> None:
        self.config = config

    def initialize(self) -> str:
        if not self.config.is_enabled():
            return "OpenTelemetry disabled"
        return "OpenTelemetry enabled (no exporters configured)"
