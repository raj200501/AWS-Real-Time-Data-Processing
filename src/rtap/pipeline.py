"""Local real-time pipeline simulation using AWS fakes."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import random
import time
from typing import Dict, Iterable, List, Optional

import boto3
import rtap.aws  # noqa: F401

from .config import RuntimeConfig
from .health import HealthStatus, build_health_status
from .logging_utils import LogContext, configure_logging
from .metrics import MetricRegistry
from .plugins.base import EventPayload
from .plugins.loader import PluginRegistry
from .policy import PolicyEngine
from .tracing import TraceRecorder


@dataclass
class PipelineResult:
    events_processed: int
    s3_object_key: str
    report: Dict[str, float | int]
    metrics_snapshot: Dict[str, float]
    health: HealthStatus


@dataclass
class EventGenerator:
    seed: int = 42
    min_temp: float = 20.0
    max_temp: float = 35.0
    min_humidity: float = 30.0
    max_humidity: float = 70.0

    def generate(self, count: int) -> List[EventPayload]:
        rng = random.Random(self.seed)
        events: List[EventPayload] = []
        for _ in range(count):
            events.append(
                EventPayload(
                    sensor_id=rng.randint(1, 5),
                    temperature=round(rng.uniform(self.min_temp, self.max_temp), 2),
                    humidity=round(
                        rng.uniform(self.min_humidity, self.max_humidity), 2
                    ),
                    timestamp=int(time.time()),
                )
            )
        return events


@dataclass
class Pipeline:
    config: RuntimeConfig
    plugins: PluginRegistry = field(default_factory=PluginRegistry)
    metrics: MetricRegistry = field(default_factory=MetricRegistry)
    trace: TraceRecorder = field(default_factory=TraceRecorder)
    policy: Optional[PolicyEngine] = None

    def __post_init__(self) -> None:
        self.metrics.enabled = self.config.metrics_enabled
        if self.config.trace_path:
            self.trace.enabled = True
            self.trace.path = self.config.trace_path
        if self.config.policy_enabled:
            if self.config.policy_allowlist:
                self.policy = PolicyEngine.from_allowlist(self.config.policy_allowlist)
            else:
                self.policy = PolicyEngine()

    def _clients(self):
        return {
            "kinesis": boto3.client("kinesis"),
            "s3": boto3.client("s3"),
            "dynamodb": boto3.client("dynamodb"),
            "lambda": boto3.client("lambda"),
        }

    def _ensure_resources(
        self, stream_name: str, bucket_name: str, table_name: str
    ) -> None:
        clients = self._clients()
        clients["kinesis"].create_stream(StreamName=stream_name, ShardCount=1)
        clients["s3"].create_bucket(Bucket=bucket_name)
        clients["dynamodb"].create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "sensor_id", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "sensor_id", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "N"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

    def _write_events_to_s3(
        self, bucket_name: str, key: str, events: Iterable[EventPayload]
    ) -> None:
        body = "\n".join(json.dumps(event.as_dict()) for event in events)
        boto3.client("s3").put_object(Bucket=bucket_name, Key=key, Body=body)

    def _store_event_in_dynamodb(self, table_name: str, payload: EventPayload) -> None:
        item = {
            "sensor_id": {"S": str(payload.sensor_id)},
            "timestamp": {"N": str(payload.timestamp)},
            "temperature": {"N": str(payload.temperature)},
            "humidity": {"N": str(payload.humidity)},
        }
        boto3.client("dynamodb").put_item(TableName=table_name, Item=item)

    def _invoke_lambda(
        self, function_name: str, payload: Dict[str, float | int]
    ) -> None:
        boto3.client("lambda").invoke(
            FunctionName=function_name, Payload=json.dumps(payload)
        )

    def run(
        self,
        *,
        stream_name: str,
        bucket_name: str,
        table_name: str,
        event_count: int = 5,
        partition_key: str = "demo",
        report_key: str = "reports/summary.json",
        trace_key: str = "reports/trace.jsonl",
        artifact_dir: Optional[Path] = None,
        seed: int = 42,
    ) -> PipelineResult:
        log_context = LogContext(component="pipeline")
        logger = configure_logging(
            json_format=self.config.log_format == "json", context=log_context
        )
        logger.info("Starting pipeline run", extra={"rtap_stream": stream_name})

        if artifact_dir is not None:
            report_key = str(Path(artifact_dir) / report_key)
            trace_key = str(Path(artifact_dir) / trace_key)

        with self.metrics.time("pipeline.setup"):
            self._ensure_resources(stream_name, bucket_name, table_name)

        generator = EventGenerator(seed=seed)
        events = generator.generate(event_count)
        clients = self._clients()

        with self.metrics.time("pipeline.ingest"):
            for event in events:
                clients["kinesis"].put_record(
                    StreamName=stream_name,
                    Data=json.dumps(event.as_dict()),
                    PartitionKey=partition_key,
                )
                self.metrics.increment("kinesis.records.sent")

        shard_iterator = clients["kinesis"].get_shard_iterator(
            StreamName=stream_name,
            ShardId="shardId-000000000000",
            ShardIteratorType="TRIM_HORIZON",
        )["ShardIterator"]

        processed: List[EventPayload] = []
        with self.metrics.time("pipeline.consume"):
            while True:
                response = clients["kinesis"].get_records(
                    ShardIterator=shard_iterator, Limit=50
                )
                records = response.get("Records", [])
                if not records:
                    break
                for record in records:
                    payload = json.loads(record["Data"])
                    event = EventPayload(
                        sensor_id=int(payload["sensor_id"]),
                        temperature=float(payload["temperature"]),
                        humidity=float(payload["humidity"]),
                        timestamp=int(payload["timestamp"]),
                    )
                    processed_event = self.plugins.process_all(event)
                    if self.policy is not None:
                        decision = self.policy.evaluate(processed_event)
                        if not decision.allowed:
                            self.metrics.increment("policy.denied")
                            continue
                        self.metrics.increment("policy.allowed")
                    processed.append(processed_event)
                    self.metrics.increment("kinesis.records.received")
                shard_iterator = response.get("NextShardIterator", shard_iterator)

        with self.metrics.time("pipeline.store"):
            for event in processed:
                self._store_event_in_dynamodb(table_name, event)
                self._invoke_lambda("rtap-processor", event.as_dict())

        report = self._build_report(processed)
        self._write_events_to_s3(bucket_name, report_key, processed)
        self._write_events_to_s3(bucket_name, trace_key, processed)

        if self.trace.enabled:
            for event in processed:
                self.trace.record_event("event.processed", payload=event.as_dict())

        metrics_snapshot = self.metrics.snapshot().summary()
        health = build_health_status(
            {
                "kinesis": True,
                "s3": True,
                "dynamodb": True,
                "lambda": True,
            }
        )

        logger.info("Pipeline run complete", extra={"rtap_processed": len(processed)})
        return PipelineResult(
            events_processed=len(processed),
            s3_object_key=report_key,
            report=report,
            metrics_snapshot=metrics_snapshot,
            health=health,
        )

    def _build_report(self, events: Iterable[EventPayload]) -> Dict[str, float | int]:
        events_list = list(events)
        if not events_list:
            return {"event_count": 0}
        avg_temp = sum(event.temperature for event in events_list) / len(events_list)
        avg_humidity = sum(event.humidity for event in events_list) / len(events_list)
        max_temp = max(event.temperature for event in events_list)
        min_temp = min(event.temperature for event in events_list)
        return {
            "event_count": len(events_list),
            "avg_temperature": round(avg_temp, 2),
            "avg_humidity": round(avg_humidity, 2),
            "max_temperature": max_temp,
            "min_temperature": min_temp,
        }
