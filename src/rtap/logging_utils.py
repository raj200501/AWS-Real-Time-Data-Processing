"""Structured logging helpers for RTAP."""

from __future__ import annotations

import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional


@dataclass
class LogContext:
    """Contextual information for structured logs."""

    service: str = "rtap"
    component: str = "core"
    environment: str = "local"
    extra: Dict[str, Any] = field(default_factory=dict)

    def with_fields(self, **fields: Any) -> "LogContext":
        merged = {**self.extra, **fields}
        return LogContext(
            service=self.service,
            component=self.component,
            environment=self.environment,
            extra=merged,
        )


class JsonLogFormatter(logging.Formatter):
    """JSON formatter for structured logs."""

    def __init__(self, context: LogContext) -> None:
        super().__init__()
        self.context = context

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": self.context.service,
            "component": self.context.component,
            "environment": self.context.environment,
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        if self.context.extra:
            payload["context"] = self.context.extra
        for key, value in record.__dict__.items():
            if key.startswith("rtap_"):
                payload[key.replace("rtap_", "")] = value
        return json.dumps(payload, ensure_ascii=False)


class TextLogFormatter(logging.Formatter):
    """Human-friendly logging format with context."""

    def __init__(self, context: LogContext) -> None:
        super().__init__("%(asctime)s %(levelname)s [%(name)s] %(message)s")
        self.context = context

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        if self.context.extra:
            message = f"{message} | context={self.context.extra}"
        for key, value in record.__dict__.items():
            if key.startswith("rtap_"):
                message = f"{message} | {key.replace('rtap_', '')}={value}"
        return message


@dataclass
class StructuredLogger:
    """Factory for logger instances with consistent formatting."""

    name: str
    context: LogContext
    json_format: bool = False

    def build(self) -> logging.Logger:
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        handler = logging.StreamHandler(sys.stdout)
        if self.json_format:
            handler.setFormatter(JsonLogFormatter(self.context))
        else:
            handler.setFormatter(TextLogFormatter(self.context))
        logger.addHandler(handler)
        logger.propagate = False
        return logger


class LogAdapter(logging.LoggerAdapter):
    """Adapter that injects structured context into log records."""

    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
        extra = kwargs.setdefault("extra", {})
        for key, value in self.extra.items():
            extra[f"rtap_{key}"] = value
        return msg, kwargs


def get_logger(
    name: str,
    *,
    json_format: bool = False,
    context: Optional[LogContext] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> logging.LoggerAdapter:
    """Return a structured logger adapter.

    Args:
        name: logger name.
        json_format: emit JSON logs when True.
        context: optional LogContext.
        extra: additional context fields.
    """

    base_context = context or LogContext()
    if extra:
        base_context = base_context.with_fields(**extra)
    logger = StructuredLogger(
        name=name, context=base_context, json_format=json_format
    ).build()
    return LogAdapter(logger, extra or {})


def configure_logging(
    *,
    json_format: bool = False,
    context: Optional[LogContext] = None,
    extra: Optional[Dict[str, Any]] = None,
    levels: Optional[Iterable[tuple[str, int]]] = None,
) -> logging.LoggerAdapter:
    """Configure root logging for RTAP runs.

    Returns a logger adapter to use for the primary component.
    """

    logger = get_logger("rtap", json_format=json_format, context=context, extra=extra)
    if levels:
        for logger_name, level in levels:
            logging.getLogger(logger_name).setLevel(level)
    return logger
