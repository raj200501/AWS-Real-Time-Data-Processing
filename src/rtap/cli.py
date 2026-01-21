"""CLI entry points for RTAP demos and diagnostics."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile

from .config import RuntimeConfig
from .health import build_health_status
from .logging_utils import configure_logging
from .metrics import format_metrics
from .pipeline import Pipeline
from .plugins.loader import PluginRegistry
from .reporting import AnalyticsReport
from .tracing import TraceExporter, TraceRecorder


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RTAP local pipeline utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo = subparsers.add_parser("demo", help="Run a local demo pipeline")
    demo.add_argument(
        "--events", type=int, default=8, help="Number of events to simulate"
    )
    demo.add_argument("--trace", action="store_true", help="Enable JSONL tracing")

    simulate = subparsers.add_parser("simulate", help="Run pipeline simulation")
    simulate.add_argument("--stream", default="demo-stream")
    simulate.add_argument("--bucket", default="demo-bucket")
    simulate.add_argument("--table", default="demo-table")
    simulate.add_argument("--events", type=int, default=5)

    report = subparsers.add_parser("report", help="Generate a report from S3 data")
    report.add_argument("--bucket", required=True)
    report.add_argument("--key", required=True)
    report.add_argument("--out", default="report.md")

    health = subparsers.add_parser("health", help="Print health status")
    health.add_argument(
        "--component", action="append", default=["kinesis", "s3", "dynamodb", "lambda"]
    )

    return parser


def _run_demo(args: argparse.Namespace) -> int:
    logger = configure_logging(
        json_format=os.getenv("RTAP_LOG_FORMAT", "text") == "json"
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        trace_path = tmp_path / "trace.jsonl" if args.trace else None
        config = RuntimeConfig.from_env().with_demo(trace_path=trace_path)
        registry = PluginRegistry()
        registry.register_builtin(["normalize_temperature", "clamp_humidity"])
        pipeline = Pipeline(config=config, plugins=registry)
        result = pipeline.run(
            stream_name="demo-stream",
            bucket_name="demo-bucket",
            table_name="demo-table",
            event_count=args.events,
            report_key="reports/events.jsonl",
        )

        report = AnalyticsReport.from_s3("demo-bucket", "reports/events.jsonl")
        report_path = tmp_path / "report.md"
        report.write_markdown(report_path)

        if trace_path:
            exporter = TraceExporter(
                events=TraceRecorder(path=trace_path, enabled=True).read_events()
            )
            export_path = tmp_path / "trace.md"
            export_path.write_text(exporter.to_markdown(), encoding="utf-8")

        print("Demo Summary")
        print("============")
        print(f"Events processed: {result.events_processed}")
        print(f"Report summary: {report.summary()}")
        print(f"Health: {result.health.status}")
        print("PASS" if result.events_processed == args.events else "FAIL")
        sys.stdout.flush()
        logger.info("Demo run complete", extra={"rtap_events": result.events_processed})
        return 0 if result.events_processed == args.events else 1


def _run_simulation(args: argparse.Namespace) -> int:
    config = RuntimeConfig.from_env()
    pipeline = Pipeline(config=config)
    result = pipeline.run(
        stream_name=args.stream,
        bucket_name=args.bucket,
        table_name=args.table,
        event_count=args.events,
        report_key="reports/events.jsonl",
    )
    print(format_metrics(pipeline.metrics.snapshot()))
    print(f"Report: {result.report}")
    return 0


def _run_report(args: argparse.Namespace) -> int:
    report = AnalyticsReport.from_s3(args.bucket, args.key)
    Path(args.out).write_text(report.to_markdown(), encoding="utf-8")
    print(f"Report written to {args.out}")
    return 0


def _run_health(args: argparse.Namespace) -> int:
    checks = {component: True for component in args.component}
    status = build_health_status(checks)
    print(status)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    configure_logging(json_format=os.getenv("RTAP_LOG_FORMAT", "text") == "json").info(
        "CLI command", extra={"rtap_command": args.command}
    )

    if args.command == "demo":
        return _run_demo(args)
    if args.command == "simulate":
        return _run_simulation(args)
    if args.command == "report":
        return _run_report(args)
    if args.command == "health":
        return _run_health(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
