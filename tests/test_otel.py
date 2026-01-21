from rtap.otel import OtelConfig, OtelScaffold


def test_otel_scaffold_disabled():
    config = OtelConfig(enabled=False)
    scaffold = OtelScaffold(config)
    assert scaffold.initialize() == "OpenTelemetry disabled"


def test_otel_scaffold_enabled():
    config = OtelConfig(enabled=True, service_name="demo", attributes={"env": "test"})
    scaffold = OtelScaffold(config)
    assert "enabled" in scaffold.initialize()
    assert config.to_resource_attributes()["service.name"] == "demo"
