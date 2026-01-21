from pathlib import Path

from rtap.tracing import TraceExporter, TraceRecorder


def test_trace_recorder_writes_events(tmp_path: Path):
    trace_path = tmp_path / "trace.jsonl"
    recorder = TraceRecorder(path=trace_path, enabled=True)

    recorder.record_event("event", value=1)
    recorder.record_event("event", value=2)

    events = recorder.read_events()
    assert len(events) == 2
    assert events[0]["payload"]["value"] == 1


def test_trace_exporter_markdown(tmp_path: Path):
    trace_path = tmp_path / "trace.jsonl"
    recorder = TraceRecorder(path=trace_path, enabled=True)
    recorder.record_event("demo", status="ok")

    exporter = TraceExporter(events=recorder.read_events())
    markdown = exporter.to_markdown()

    assert "Trace Export" in markdown
    assert "demo" in markdown
