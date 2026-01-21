from rtap.metrics import MetricRegistry, merge_snapshots


def test_merge_snapshots_combines_counts():
    reg_a = MetricRegistry()
    reg_b = MetricRegistry()
    reg_a.increment("events", 2)
    reg_b.increment("events", 3)
    reg_a.observe("latency", 0.1)
    reg_b.observe("latency", 0.2)

    merged = merge_snapshots([reg_a.snapshot(), reg_b.snapshot()])

    assert merged.counters["events"] == 5
    assert len(merged.timers["latency"]) == 2
