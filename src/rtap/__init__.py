"""RTAP: local real-time analytics tooling for the AWS sample project."""

from __future__ import annotations

from .config import RuntimeConfig
from .pipeline import Pipeline, PipelineResult
from .reporting import AnalyticsReport

__all__ = ["RuntimeConfig", "Pipeline", "PipelineResult", "AnalyticsReport"]
__version__ = "0.1.0"
