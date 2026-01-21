from rtap.config import RuntimeConfig
from rtap.pipeline import Pipeline
from rtap.plugins.loader import PluginRegistry


def test_pipeline_runs_with_fake_aws(monkeypatch, tmp_path):
    monkeypatch.setenv("USE_FAKE_AWS", "1")
    monkeypatch.setenv("RTAP_TRACE_PATH", str(tmp_path / "trace.jsonl"))

    config = RuntimeConfig.from_env()
    registry = PluginRegistry()
    registry.register_builtin(["normalize_temperature", "clamp_humidity"])
    pipeline = Pipeline(config=config, plugins=registry)

    result = pipeline.run(
        stream_name="test-stream",
        bucket_name="test-bucket",
        table_name="test-table",
        event_count=4,
        report_key="reports/events.jsonl",
    )

    assert result.events_processed == 4
    assert result.report["event_count"] == 4
    assert result.health.status == "ok"
