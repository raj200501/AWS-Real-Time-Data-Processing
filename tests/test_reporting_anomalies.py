from rtap.reporting import AnalyticsReport


def test_report_anomalies_detected():
    lines = "\n".join(
        [
            '{"sensor_id": 1, "temperature": 20.0, "humidity": 40.0, "timestamp": 1}',
            '{"sensor_id": 2, "temperature": 34.0, "humidity": 70.0, "timestamp": 2}',
        ]
    )
    report = AnalyticsReport.from_json_lines(lines)
    anomalies = report.anomalies(temp_threshold=33.0, humidity_threshold=65.0)

    assert len(anomalies) == 1
    assert anomalies[0].sensor_id == 2
