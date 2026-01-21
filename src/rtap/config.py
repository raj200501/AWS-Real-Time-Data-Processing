"""Runtime configuration and feature flags for the RTAP toolkit."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class RuntimeConfig:
    """Configuration flags that control optional functionality.

    All optional features are off by default. They can be enabled via
    environment variables or CLI flags for demo and diagnostics.
    """

    use_fake_aws: bool = True
    log_format: str = "text"
    trace_path: Optional[Path] = None
    otel_enabled: bool = False
    metrics_enabled: bool = True
    demo_mode: bool = False
    policy_enabled: bool = False
    policy_allowlist: Optional[tuple[int, ...]] = None

    @staticmethod
    def from_env() -> "RuntimeConfig":
        """Create a RuntimeConfig from environment variables."""
        use_fake_aws = os.getenv("USE_FAKE_AWS", "1") == "1"
        log_format = os.getenv("RTAP_LOG_FORMAT", "text").lower()
        trace_value = os.getenv("RTAP_TRACE_PATH", "").strip()
        trace_path = Path(trace_value) if trace_value else None
        otel_enabled = os.getenv("RTAP_OTEL", "0") == "1"
        metrics_enabled = os.getenv("RTAP_METRICS", "1") == "1"
        demo_mode = os.getenv("RTAP_DEMO_MODE", "0") == "1"
        policy_enabled = os.getenv("RTAP_POLICY", "0") == "1"
        allowlist_raw = os.getenv("RTAP_POLICY_ALLOWLIST", "").strip()
        policy_allowlist = (
            tuple(int(item) for item in allowlist_raw.split(",") if item.strip())
            or None
        )
        return RuntimeConfig(
            use_fake_aws=use_fake_aws,
            log_format=log_format,
            trace_path=trace_path,
            otel_enabled=otel_enabled,
            metrics_enabled=metrics_enabled,
            demo_mode=demo_mode,
            policy_enabled=policy_enabled,
            policy_allowlist=policy_allowlist,
        )

    def with_demo(self, trace_path: Optional[Path] = None) -> "RuntimeConfig":
        """Return a demo-friendly configuration without mutating the original."""
        return RuntimeConfig(
            use_fake_aws=self.use_fake_aws,
            log_format=self.log_format,
            trace_path=trace_path if trace_path is not None else self.trace_path,
            otel_enabled=self.otel_enabled,
            metrics_enabled=self.metrics_enabled,
            demo_mode=True,
            policy_enabled=self.policy_enabled,
            policy_allowlist=self.policy_allowlist,
        )
