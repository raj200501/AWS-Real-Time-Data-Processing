from rtap.config import RuntimeConfig
from rtap.pipeline import Pipeline


def test_pipeline_report_contains_stats(monkeypatch):
    monkeypatch.setenv("USE_FAKE_AWS", "1")
    config = RuntimeConfig.from_env()
    pipeline = Pipeline(config=config)

    result = pipeline.run(
        stream_name="stats-stream",
        bucket_name="stats-bucket",
        table_name="stats-table",
        event_count=2,
        report_key="reports/events.jsonl",
    )

    assert result.report["event_count"] == 2
    assert "avg_temperature" in result.report
