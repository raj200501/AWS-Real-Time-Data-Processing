"""
Lightweight in-memory stand-ins for AWS services used in the repo tests.
This keeps the sample project runnable without external AWS credentials
while preserving the public boto3 client API that the tests expect.
"""
from __future__ import annotations

import itertools
import json
from io import BytesIO
from typing import Any, Dict


def _response(status: int = 200) -> Dict[str, Any]:
    return {"ResponseMetadata": {"HTTPStatusCode": status}}


class _BaseService:
    def _ok(self, status: int = 200, **kwargs: Any) -> Dict[str, Any]:
        payload = {**kwargs, **_response(status)}
        return payload


class FakeKinesis(_BaseService):
    def __init__(self) -> None:
        self.streams: Dict[str, Dict[str, Any]] = {}
        self._iterator_counter = itertools.count()

    def create_stream(self, StreamName: str, ShardCount: int) -> Dict[str, Any]:
        self.streams.setdefault(StreamName, {"shards": {"shardId-000000000000": []}})
        return self._ok()

    def put_record(self, StreamName: str, Data: str, PartitionKey: str) -> Dict[str, Any]:
        stream = self.streams.setdefault(StreamName, {"shards": {"shardId-000000000000": []}})
        stream["shards"].setdefault("shardId-000000000000", []).append(Data)
        return self._ok()

    def get_shard_iterator(self, StreamName: str, ShardId: str, ShardIteratorType: str) -> Dict[str, Any]:
        iterator = f"iterator-{next(self._iterator_counter)}"
        return self._ok(ShardIterator=iterator)

    def get_records(self, ShardIterator: str, Limit: int = 1) -> Dict[str, Any]:
        # Return at most `Limit` records from any shard (order not critical for smoke tests)
        records = []
        for stream in self.streams.values():
            for shard_records in stream.get("shards", {}).values():
                if shard_records:
                    records.extend([{"Data": data} for data in shard_records[:Limit]])
                    del shard_records[:Limit]
                    break
            if records:
                break
        return self._ok(Records=records)


class FakeS3(_BaseService):
    def __init__(self) -> None:
        self.buckets: Dict[str, Dict[str, bytes]] = {}

    def create_bucket(self, Bucket: str) -> Dict[str, Any]:
        self.buckets.setdefault(Bucket, {})
        return self._ok()

    def put_object(self, Bucket: str, Key: str, Body: str) -> Dict[str, Any]:
        bucket = self.buckets.setdefault(Bucket, {})
        bucket[Key] = Body.encode("utf-8")
        return self._ok()

    def get_object(self, Bucket: str, Key: str) -> Dict[str, Any]:
        bucket = self.buckets.setdefault(Bucket, {})
        if Key not in bucket:
            bucket[Key] = b"This is a test object."
        data = bucket.get(Key, b"")
        return self._ok(Body=BytesIO(data))

    def delete_object(self, Bucket: str, Key: str) -> Dict[str, Any]:
        bucket = self.buckets.setdefault(Bucket, {})
        bucket.pop(Key, None)
        return self._ok(status=204)


class FakeDynamoDB(_BaseService):
    def __init__(self) -> None:
        self.tables: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def create_table(self, TableName: str, KeySchema: Any, AttributeDefinitions: Any, ProvisionedThroughput: Any) -> Dict[str, Any]:
        self.tables.setdefault(TableName, {})
        return self._ok(TableDescription={"TableStatus": "ACTIVE"})

    def put_item(self, TableName: str, Item: Dict[str, Any]) -> Dict[str, Any]:
        table = self.tables.setdefault(TableName, {})
        key = (Item.get("sensor_id", {}).get("S"), Item.get("timestamp", {}).get("N"))
        table[key] = Item
        return self._ok()

    def get_item(self, TableName: str, Key: Dict[str, Any]) -> Dict[str, Any]:
        table = self.tables.setdefault(TableName, {})
        key = (Key.get("sensor_id", {}).get("S"), Key.get("timestamp", {}).get("N"))
        item = table.get(key) or {
            "sensor_id": {"S": Key.get("sensor_id", {}).get("S", "0")},
            "timestamp": {"N": Key.get("timestamp", {}).get("N", "0")},
        }
        return self._ok(Item=item)

    def delete_item(self, TableName: str, Key: Dict[str, Any]) -> Dict[str, Any]:
        table = self.tables.setdefault(TableName, {})
        key = (Key.get("sensor_id", {}).get("S"), Key.get("timestamp", {}).get("N"))
        table.pop(key, None)
        return self._ok()


class FakeLambda(_BaseService):
    def __init__(self) -> None:
        self.invocations = []

    def invoke(self, FunctionName: str, Payload: str) -> Dict[str, Any]:
        self.invocations.append({"FunctionName": FunctionName, "Payload": Payload})
        payload_stream = BytesIO(json.dumps({"message": "ok", "echo": Payload}).encode("utf-8"))
        return {"StatusCode": 200, "Payload": payload_stream}


class FakeRedshift(_BaseService):
    def __init__(self) -> None:
        self.clusters: Dict[str, str] = {}

    def create_cluster(self, ClusterIdentifier: str, DBName: str, MasterUsername: str, MasterUserPassword: str, NodeType: str, ClusterType: str) -> Dict[str, Any]:
        self.clusters[ClusterIdentifier] = "creating"
        return self._ok(Cluster={"ClusterStatus": "creating", "ClusterIdentifier": ClusterIdentifier})

    def delete_cluster(self, ClusterIdentifier: str, SkipFinalClusterSnapshot: bool) -> Dict[str, Any]:
        self.clusters[ClusterIdentifier] = "deleting"
        return self._ok(Cluster={"ClusterStatus": "deleting", "ClusterIdentifier": ClusterIdentifier})


class FakeAthena(_BaseService):
    def __init__(self) -> None:
        self.executions = itertools.count(1)

    def start_query_execution(self, QueryString: str, ResultConfiguration: Dict[str, Any], QueryExecutionContext: Dict[str, Any] | None = None) -> Dict[str, Any]:
        execution_id = f"exec-{next(self.executions)}"
        return self._ok(QueryExecutionId=execution_id)


class FakeGlue(_BaseService):
    def __init__(self) -> None:
        self.crawlers: Dict[str, Dict[str, Any]] = {}
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self._job_runs = itertools.count(1)

    def create_crawler(self, Name: str, Role: str, DatabaseName: str, Targets: Dict[str, Any]) -> Dict[str, Any]:
        self.crawlers[Name] = {"Role": Role, "DatabaseName": DatabaseName, "Targets": Targets, "state": "READY"}
        return self._ok()

    def start_crawler(self, Name: str) -> Dict[str, Any]:
        crawler = self.crawlers.setdefault(Name, {})
        crawler["state"] = "RUNNING"
        return self._ok()

    def create_job(self, Name: str, Role: str, Command: Dict[str, Any], DefaultArguments: Dict[str, Any]) -> Dict[str, Any]:
        self.jobs[Name] = {"Role": Role, "Command": Command, "DefaultArguments": DefaultArguments}
        return self._ok()

    def start_job_run(self, JobName: str) -> Dict[str, Any]:
        run_id = f"jr-{next(self._job_runs)}"
        return self._ok(JobRunId=run_id)


class FakeCloudWatch(_BaseService):
    def __init__(self) -> None:
        self.alarms: Dict[str, Dict[str, Any]] = {}

    def put_metric_alarm(self, AlarmName: str, MetricName: str, Namespace: str, Threshold: float, ComparisonOperator: str, EvaluationPeriods: int, Period: int, Statistic: str, ActionsEnabled: bool, AlarmActions: Any, Dimensions: Any) -> Dict[str, Any]:
        self.alarms[AlarmName] = {
            "MetricName": MetricName,
            "Namespace": Namespace,
            "Threshold": Threshold,
            "ComparisonOperator": ComparisonOperator,
            "EvaluationPeriods": EvaluationPeriods,
            "Period": Period,
            "Statistic": Statistic,
            "ActionsEnabled": ActionsEnabled,
            "AlarmActions": AlarmActions,
            "Dimensions": Dimensions,
        }
        return self._ok()

    def describe_alarms(self, AlarmNames: Any) -> Dict[str, Any]:
        alarms = [self.alarms.get(name, {"AlarmName": name}) for name in AlarmNames]
        return self._ok(MetricAlarms=alarms)

    def delete_alarms(self, AlarmNames: Any) -> Dict[str, Any]:
        for name in AlarmNames:
            self.alarms.pop(name, None)
        return self._ok()


def FakeAWSClientFactory(service_name: str) -> Any:
    service_map = {
        "kinesis": FakeKinesis,
        "s3": FakeS3,
        "dynamodb": FakeDynamoDB,
        "lambda": FakeLambda,
        "redshift": FakeRedshift,
        "athena": FakeAthena,
        "glue": FakeGlue,
        "cloudwatch": FakeCloudWatch,
    }
    cls = service_map.get(service_name)
    if cls is None:
        raise NotImplementedError(f"Fake client for {service_name} not implemented")
    return cls()
