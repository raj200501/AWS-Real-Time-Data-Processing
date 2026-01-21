from rtap.reporting import AnalyticsReport


def test_report_summary_and_markdown():
    lines = "\n".join(
        [
            '{"sensor_id": 1, "temperature": 20.0, "humidity": 40.0, "timestamp": 1}',
            '{"sensor_id": 1, "temperature": 25.0, "humidity": 45.0, "timestamp": 2}',
            '{"sensor_id": 2, "temperature": 35.0, "humidity": 60.0, "timestamp": 3}',
        ]
    )
    report = AnalyticsReport.from_json_lines(lines)
    summary = report.summary()

    assert summary["event_count"] == 3
    assert summary["max_temperature"] == 35.0
    assert report.sensor_breakdown()[1] == 2

    markdown = report.to_markdown()
    assert "Analytics Report" in markdown
    assert "Sensor 1" in markdown
