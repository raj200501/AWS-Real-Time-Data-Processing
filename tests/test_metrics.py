from rtap.metrics import MetricRegistry, format_metrics


def test_metric_registry_counts_and_timers():
    registry = MetricRegistry()
    registry.increment("events", 3)
    with registry.time("operation"):
        pass
    snapshot = registry.snapshot()

    assert snapshot.counters["events"] == 3
    assert "operation" in snapshot.timers
    assert len(snapshot.timers["operation"]) == 1


def test_format_metrics_output():
    registry = MetricRegistry()
    registry.increment("events", 1)
    registry.observe("latency", 0.25)
    output = format_metrics(registry.snapshot())

    assert "rtap.events.count" in output
    assert "rtap.latency.avg_s" in output
